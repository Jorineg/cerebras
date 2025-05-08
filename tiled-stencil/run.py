#!/usr/bin/env cs_python

WEIGHTS = [1.0, 0.5]

import argparse
import json
import numpy as np

from cerebras.sdk.runtime.sdkruntimepybind import (
    SdkRuntime,
    MemcpyDataType,
    MemcpyOrder,
)  # pylint: disable=no-name-in-module

from stencil import star_stencil, print_matrix

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("--name", help="the test compile output dir")
parser.add_argument("--cmaddr", help="IP:port for CS system")
args = parser.parse_args()

# Get matrix dimensions from compile metadata
with open(f"{args.name}/out.json", encoding="utf-8") as json_file:
    compile_data = json.load(json_file)

# Matrix dimensions
width = int(compile_data["params"]["w"])
height = int(compile_data["params"]["h"])
tile_width = int(compile_data["params"]["tile_width"])
tile_height = int(compile_data["params"]["tile_height"])
rank = int(compile_data["params"]["rank"])
num_iterations = int(compile_data["params"]["num_iterations"])

w_compute_region_py = width - 2 * (rank - 1)
h_compute_region_py = height - 2 * (rank - 1)

num_pe_x_inner_py = w_compute_region_py // tile_width
num_pe_y_inner_py = h_compute_region_py // tile_height

num_pe_x = num_pe_x_inner_py + 2  # Total PEs including border
num_pe_y = num_pe_y_inner_py + 2  # Total PEs including border

print(f"Using original matrix of size {width}x{height} for {num_iterations} iterations")
print(f"Tile size: {tile_width}x{tile_height}")
print(f"Rank: {rank}")
print(f"PE grid dimensions: {num_pe_x}x{num_pe_y} (includes border PEs)")
print(f"Computational region (inner PEs cover): {w_compute_region_py}x{h_compute_region_py} elements")

# Create random matrix with integers of size (width, height)
matrix = np.random.randint(0, 10, (height, width)).astype(np.float32)

# Print the matrix
print_matrix(matrix, "Original Matrix")

# Run the stencil computation on host for verification
result_expected = star_stencil(matrix, WEIGHTS, num_iterations)

# Print the result
print_matrix(result_expected, "Result Matrix (python computation)")

# Construct a runner using SdkRuntime
runner = SdkRuntime(args.name, cmaddr=args.cmaddr)

# Get symbols on device
matrix_symbol = runner.get_id("values")
weights_symbol = runner.get_id("weights")

# Load and run the program
runner.load()
runner.run()

# repeat weights for each PE
pe_weights = np.repeat(WEIGHTS, num_pe_x * num_pe_y).astype(np.float32)

# copy weights to device
runner.memcpy_h2d(
    weights_symbol,
    pe_weights,
    0,
    0,
    num_pe_x,
    num_pe_y,
    len(WEIGHTS), # This is the size of the weights array for one PE
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)
print("copied weights to device")

def tile_matrix(m_orig, current_rank, current_tile_width, current_tile_height, current_num_pe_y, current_num_pe_x):
    # Symmetric padding amounts to correctly position m_orig within the PE grid canvas.
    # tile_dim - (rank-1) ensures m_orig[rank-1,rank-1] maps to the start of PE(1,1)'s tile data.
    # Assertions: rank >= 1 and tile_dim >= rank (from CSL) ensure pad_y/pad_x >= 1.
    pad_y = current_tile_height - (current_rank - 1)
    pad_x = current_tile_width - (current_rank - 1)

    canvas = np.pad(m_orig,
                      ((pad_y, pad_y), (pad_x, pad_x)), # Apply symmetric padding
                      mode='constant',
                      constant_values=0)

    # The dimensions of 'canvas' will be (current_num_pe_y * current_tile_height, current_num_pe_x * current_tile_width)
    # due to the relationship between num_pe_dims, orig matrix dims, rank, and tile_dims established in layout.csl.

    reshaped = canvas.reshape(current_num_pe_y, current_tile_height, current_num_pe_x, current_tile_width)
    swapped = reshaped.swapaxes(1, 2) # num_pe_y, num_pe_x, tile_height, tile_width
    return swapped.flatten()

def untile_matrix(m_flat, current_rank, current_tile_width, current_tile_height, current_num_pe_y, current_num_pe_x):
    h_device_grid = current_num_pe_y * current_tile_height
    w_device_grid = current_num_pe_x * current_tile_width
    
    reshaped_from_flat = m_flat.reshape(current_num_pe_y, current_num_pe_x, current_tile_height, current_tile_width)
    swapped_back = reshaped_from_flat.swapaxes(1, 2) 
    canvas_reconstructed = swapped_back.reshape(h_device_grid, w_device_grid)

    # Slice out the original matrix using the same symmetric padding values.
    slice_y = current_tile_height - (current_rank - 1)
    slice_x = current_tile_width - (current_rank - 1)
    
    m_original = canvas_reconstructed[slice_y : -slice_y, slice_x : -slice_x]
    return m_original

# data must be one-dimensional so flatten the matrix
# Pass all necessary current values to tile_matrix
device_matrix = tile_matrix(matrix, rank, tile_width, tile_height, num_pe_y, num_pe_x)


# Copy matrix into matrix of PEs
runner.memcpy_h2d(
    matrix_symbol,
    device_matrix, # This is already flattened and tiled correctly for the whole grid
    0, # dest_x
    0, # dest_y
    num_pe_x, # width_in_pes
    num_pe_y, # height_in_pes
    tile_width * tile_height, # num_elements_per_pe
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

print("copied matrix to device")

# Launch the compute function on device
runner.launch("compute", nonblock=False)

print("launched compute on device")

# Allocate space for result from device (entire PE grid's data)
result_device_flat = np.zeros(num_pe_y * num_pe_x * tile_height * tile_width, dtype=np.float32)

runner.memcpy_d2h(
    result_device_flat,
    matrix_symbol,
    0, # src_x
    0, # src_y
    num_pe_x, # width_in_pes
    num_pe_y, # height_in_pes
    tile_width * tile_height, # num_elements_per_pe
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

# Untile the result, passing original dimensions height, width
result = untile_matrix(result_device_flat, rank, tile_width, tile_height, num_pe_y, num_pe_x)

print("copied result from device")

# Stop the program
runner.stop()

print_matrix(result, "Result Matrix (device computation)")

# Ensure that the result matches our expectation
# Note: The python star_stencil computes on the original (H_orig_py, W_orig_py) matrix.
# The device computation, after untiling, should yield results matching this for the
# same (H_orig_py, W_orig_py) region.
if result.shape != result_expected.shape:
    raise AssertionError(f"Shape mismatch! Device result: {result.shape}, Expected: {result_expected.shape}")

np.testing.assert_allclose(result, result_expected, atol=0.01, rtol=0)
print("SUCCESS!")
