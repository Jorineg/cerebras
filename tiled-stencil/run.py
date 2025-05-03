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
num_pe_x = width // tile_width
num_pe_y = height // tile_height

print(f"Using matrix of size {width}x{height} for {num_iterations} iterations")
print(f"Tile size: {tile_width}x{tile_height}")
print(f"Rank: {rank}")
print(f"Number of PEs: {num_pe_x}x{num_pe_y}")

# Create random matrix with integers of size (width, height)
matrix = np.random.randint(0, 10, (height, width)).astype(np.float32)

# Print the matrix
print_matrix(matrix, "Original Matrix")

# Run the stencil computation
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

def tile_matrix(m, tile_width, tile_height, num_x_tiles, num_y_tiles):
    reshaped = m.reshape(num_y_tiles, tile_height, num_x_tiles, tile_width)
    swapped = reshaped.swapaxes(1, 2)
    return swapped.flatten()

def untile_matrix(m, tile_width, tile_height, num_x_tiles, num_y_tiles):
    reshaped = m.reshape(num_y_tiles, num_x_tiles, tile_height, tile_width)
    swapped = reshaped.swapaxes(1, 2)
    return swapped.reshape(num_y_tiles * tile_height, num_x_tiles * tile_width)

# data must be one-dimensional so flatten the matrix
device_matrix = tile_matrix(matrix, tile_width, tile_height, num_pe_x, num_pe_y)

# Copy matrix into matrix of PEs (0, 0) and y of PE (1, 0)
runner.memcpy_h2d(
    matrix_symbol,
    device_matrix,
    0,
    0,
    num_pe_x,
    num_pe_y,
    tile_width * tile_height,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

print("copied matrix to device")

# Launch the compute function on device
runner.launch("compute", nonblock=False)

print("launched compute on device")

# Copy y back from PE (1, 0)
result = np.zeros(width * height, dtype=np.float32)
runner.memcpy_d2h(
    result,
    matrix_symbol,
    0,
    0,
    num_pe_x,
    num_pe_y,
    tile_width * tile_height,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

# reshape the result
result = untile_matrix(result, tile_width, tile_height, num_pe_x, num_pe_y)

print("copied result from device")

# Stop the program
runner.stop()

print_matrix(result, "Result Matrix (device computation)")

# Ensure that the result matches our expectation
np.testing.assert_allclose(result, result_expected, atol=0.01, rtol=0)
print("SUCCESS!")
