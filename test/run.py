#!/usr/bin/env cs_python

import argparse
import json
import numpy as np

from cerebras.sdk.runtime.sdkruntimepybind import (
    SdkRuntime,
    MemcpyDataType,
    MemcpyOrder,
)  # pylint: disable=no-name-in-module

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("--name", help="the test compile output dir")
parser.add_argument("--cmaddr", help="IP:port for CS system")
args = parser.parse_args()

# Get matrix dimensions from compile metadata
with open(f"{args.name}/out.json", encoding="utf-8") as json_file:
    compile_data = json.load(json_file)

# Matrix dimensions
M = int(compile_data["params"]["M"])

# Construct A, x, b
x = np.full(shape=M, fill_value=3.0, dtype=np.float32)
y = np.full(shape=M, fill_value=2.0, dtype=np.float32)

# elementwise multiplication
result_expected = x * y

# Construct a runner using SdkRuntime
runner = SdkRuntime(args.name, cmaddr=args.cmaddr)

# Get symbols for A, x, y on device
x_symbol = runner.get_id("x")
y_symbol = runner.get_id("y")
result_symbol = runner.get_id("result")

# Load and run the program
runner.load()
runner.run()

# Copy y into y of PE (0, 0) and y of PE (1, 0)
runner.memcpy_h2d(
    y_symbol,
    np.tile(y, 2),
    0,
    0,
    2,
    1,
    M,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_16BIT,
    nonblock=False,
)

# Copy x into x of PE (0, 0) and x of PE (1, 0)
runner.memcpy_h2d(
    x_symbol,
    np.tile(x, 2),
    0,
    0,
    2,
    1,
    M,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_16BIT,
    nonblock=False,
)

# Launch the compute function on device
runner.launch("compute", nonblock=False)

# Copy y back from PE (1, 0)
result = np.zeros([M], dtype=np.float32)
runner.memcpy_d2h(
    result,
    result_symbol,
    1,
    0,
    1,
    1,
    M,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_16BIT,
    nonblock=False,
)

# Stop the program
runner.stop()

# Ensure that the result matches our expectation
np.testing.assert_allclose(result, result_expected, atol=0.01, rtol=0)
print("SUCCESS!")
