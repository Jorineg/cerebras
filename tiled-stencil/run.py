#!/usr/bin/env cs_python
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL/headless environments
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from cerebras.sdk.runtime.sdkruntimepybind import (
    SdkRuntime,
    MemcpyDataType,
    MemcpyOrder,
)  # pylint: disable=no-name-in-module

from stencil import star_stencil, print_matrix

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("--name", help="the test compile output dir")
parser.add_argument("--num-iterations", type=int, default=1)
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
radius = int(compile_data["params"]["radius"])
num_iterations = args.num_iterations

WEIGHTS = [1/2**i for i in range(radius+1)]

assert radius == len(WEIGHTS) - 1, "radius must be equal to the number of weights - 1"

w_compute_region_py = width - 2 * radius
h_compute_region_py = height - 2 * radius

num_pe_x_inner_py = w_compute_region_py // tile_width
num_pe_y_inner_py = h_compute_region_py // tile_height

num_pe_x = num_pe_x_inner_py + 2  # Total PEs including border
num_pe_y = num_pe_y_inner_py + 2  # Total PEs including border

print(f"Using original matrix of size {width}x{height} for {num_iterations} iterations")
print(f"Tile size: {tile_width}x{tile_height}")
print(f"radius: {radius}")
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
buffer_symbol = runner.get_id("buffer")
weights_symbol = runner.get_id("weights")

# Load and run the program
runner.load()
runner.run()

# repeat weights for each PE
pe_weights = np.tile(WEIGHTS, num_pe_x * num_pe_y).astype(np.float32)

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

def create_padded_device_matrix(m_orig, current_radius, current_tile_width, current_tile_height, current_num_pe_y, current_num_pe_x):
    """
    Tiles the original matrix and adds padding to each tile to match the device memory layout.
    """
    pad_y_canvas = current_tile_height - current_radius
    pad_x_canvas = current_tile_width - current_radius
    canvas = np.pad(m_orig, ((pad_y_canvas, pad_y_canvas), (pad_x_canvas, pad_x_canvas)), mode='constant')
    
    # split into tiles -> (num_pe_y, tile_height, num_pe_x, tile_width)
    unpadded_tiles = canvas.reshape(current_num_pe_y, current_tile_height, current_num_pe_x, current_tile_width).swapaxes(1, 2)
    
    # add padding to each tile -> (num_pe_y, tile_height, num_pe_x, tile_width)
    padded_tiles = np.pad(
        unpadded_tiles, 
        (
            (0, 0), # no padding for the PE-Grid-Dimension y
            (0, 0), # no padding for the PE-Grid-Dimension x
            (current_radius, current_radius), # padding for tile_height
            (current_radius, current_radius+1)  # padding for tile_width
        ),
        mode='constant'
    )
    
    # flatten the matrix to be able to memcpy it to the device
    return padded_tiles.flatten()


def untile_padded_matrix(m_flat_padded, current_radius, current_tile_width, current_tile_height, current_num_pe_y, current_num_pe_x):
    """
    Takes the flattened, padded data from the device, removes padding from each tile,
    and reconstructs the original matrix.
    """
    # reshape the padded matrix to 4D
    padded_tile_h = current_tile_height + 2 * current_radius
    padded_tile_w = current_tile_width + 2 * current_radius + 1
    padded_4d = m_flat_padded.reshape(current_num_pe_y, current_num_pe_x, padded_tile_h, padded_tile_w)

    # remove the padding from each tile by slicing
    unpadded_4d = padded_4d[:, :, current_radius:padded_tile_h-current_radius, current_radius:padded_tile_w-current_radius-1]

    # swap the axes to get the tiles back in the correct order
    swapped_back = unpadded_4d.swapaxes(1, 2)
    h_device_grid = current_num_pe_y * current_tile_height
    w_device_grid = current_num_pe_x * current_tile_width
    canvas_reconstructed = swapped_back.reshape(h_device_grid, w_device_grid)

    slice_y = current_tile_height - current_radius
    slice_x = current_tile_width - current_radius
    
    # slice out the original matrix from the canvas
    m_original = canvas_reconstructed[slice_y : len(canvas_reconstructed) - slice_y, slice_x : len(canvas_reconstructed[0]) - slice_x]
    return m_original


# data must be one-dimensional so flatten the matrix
# Pass all necessary current values to tile_matrix
device_matrix = create_padded_device_matrix(matrix, radius, tile_width, tile_height, num_pe_y, num_pe_x)


# Copy matrix into matrix of PEs
runner.memcpy_h2d(
    buffer_symbol,
    device_matrix, # This is already flattened and tiled correctly for the whole grid
    0, # dest_x
    0, # dest_y
    num_pe_x, # width_in_pes
    num_pe_y, # height_in_pes
    (tile_width + 2*radius+1) * (tile_height + 2*radius), # num_elements_per_pe
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

print("copied matrix to device")

# Launch the start function on device
runner.launch("start", num_iterations, nonblock=False)

print("launched compute on device")

# Allocate space for result from device (entire PE grid's data)
result_device_flat = np.zeros(num_pe_y * num_pe_x * (tile_height + 2*radius) * (tile_width + 2*radius+1), dtype=np.float32)

runner.memcpy_d2h(
    result_device_flat,
    buffer_symbol,
    0, # src_x
    0, # src_y
    num_pe_x, # width_in_pes
    num_pe_y, # height_in_pes
    (tile_width + 2*radius+1) * (tile_height + 2*radius), # num_elements_per_pe
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

# Untile the result, passing original dimensions height, width
result = untile_padded_matrix(result_device_flat, radius, tile_width, tile_height, num_pe_y, num_pe_x)

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

try:
    np.testing.assert_allclose(result, result_expected, atol=0.01, rtol=0)
    print("SUCCESS!")
except AssertionError as e:
    print(f"Results do not match! {e}")
    
    # Calculate the error per element
    error_matrix = np.abs(result - result_expected)
    
    # Create a heatmap of the error
    plt.figure(figsize=(12, 8))
    im = plt.imshow(error_matrix, cmap='viridis', aspect='equal')
    plt.colorbar(im, label='Absolute Error')
    plt.title('Error per Element (|Device Result - Expected Result|)')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    
    # Add black grid lines between pixels
    ax = plt.gca()
    ax.set_xticks(np.arange(-0.5, error_matrix.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, error_matrix.shape[0], 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)
    
    for pe_y in range(num_pe_y_inner_py):
        for pe_x in range(num_pe_x_inner_py):
            # Calculate matrix coordinates for this PE with border offset
            start_x = radius + pe_x * tile_width - 0.5
            start_y = radius + pe_y * tile_height - 0.5
            
            # Create red rectangle around this PE's tile
            rect = Rectangle((start_x, start_y), tile_width, tile_height,
                           linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect)
    
    # Save the heatmap as PNG
    plt.savefig('error_heatmap.png', dpi=500, bbox_inches='tight')
    print("Error heatmap saved as 'error_heatmap.png'")
    
    # Also save a summary
    print(f"Maximum error: {np.max(error_matrix):.6f}")
    print(f"Mean error: {np.mean(error_matrix):.6f}")
    print(f"Number of elements with error > 0.01: {np.sum(error_matrix > 0.01)}")
    
    plt.close()

    raise e
