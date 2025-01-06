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
num_steps = int(compile_data["params"]["steps"])

print(f"Using matrix of size {width}x{height} for {num_steps} steps")

# Create random matrix with integers of size (width, height)
matrix = np.random.randint(0, 10, (width, height)).astype(np.float32)

# Print the matrix
print_matrix(matrix, "Original Matrix")

# Run the stencil computation
result_expected = star_stencil(matrix, WEIGHTS, num_steps)

# Print the result
print_matrix(result_expected, "Result Matrix (python computation)")

# Construct a runner using SdkRuntime
runner = SdkRuntime(args.name, cmaddr=args.cmaddr)

# Get symbols on device
matrix_symbol = runner.get_id("matrix")

# Load and run the program
runner.load()
runner.run()

# data must be one-dimensional so flatten the matrix
device_matrix = matrix.flatten()

# Copy matrix into matrix of PEs (0, 0) and y of PE (1, 0)
runner.memcpy_h2d(
    matrix_symbol,
    device_matrix,
    0,
    0,
    width,
    height,
    1,
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
    width,
    height,
    1,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

# reshape the result
result = result.reshape(width, height)

print("copied result from device")

# Stop the program
runner.stop()

print_matrix(result, "Result Matrix (device computation)")

# Ensure that the result matches our expectation
np.testing.assert_allclose(result, result_expected, atol=0.01, rtol=0)
print("SUCCESS!")
