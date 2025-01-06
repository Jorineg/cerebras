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
length = int(compile_data["params"]["length"])

# Construct a runner using SdkRuntime
runner = SdkRuntime(args.name, cmaddr=args.cmaddr)

sart_symbol = runner.get_id("start")
value_symbol = runner.get_id("value")

# Load and run the program
runner.load()
runner.run()

# Launch the compute function on device
runner.launch("start", nonblock=False)

# Copy value back from PE (length, 0)
y_result = np.zeros([10], dtype=np.float32)
runner.memcpy_d2h(
    y_result,
    value_symbol,
    length - 1,
    0,
    1,
    1,
    10,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_16BIT,
    nonblock=False,
)

raw_bytes = y_result.tobytes()
raw_uint16 = np.frombuffer(raw_bytes, dtype=np.uint16)
lower_half = raw_uint16[::2]  # lower 2 bytes
float16_from_lower = lower_half.view(dtype=np.float16)

print("lower: ", float16_from_lower)

# Stop the program
runner.stop()

expected = np.array([10 * i + length - 2 for i in range(10)])

# Ensure that the result matches our expectation
np.testing.assert_allclose(float16_from_lower, expected, atol=0.01, rtol=0)
print("SUCCESS!")
