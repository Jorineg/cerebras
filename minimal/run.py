#!/usr/bin/env cs_python
import numpy as np

from cerebras.sdk.runtime.sdkruntimepybind import (
    SdkRuntime,
    MemcpyDataType,
    MemcpyOrder,
)  # pylint: disable=no-name-in-module

runner = SdkRuntime("out")

# Load and run the program
runner.load()
runner.run()

# Launch the compute function on device
runner.launch("start", nonblock=False)

print("started on device")

value = np.array([1.0], dtype=np.float32)

# Copy y back from PE (1, 0)
result = np.zeros(1, dtype=np.float32)
runner.memcpy_d2h(
    result,
    value,
    0,
    0,
    1,
    1,
    1,
    streaming=False,
    order=MemcpyOrder.ROW_MAJOR,
    data_type=MemcpyDataType.MEMCPY_32BIT,
    nonblock=False,
)

print("copied result value from device")
print("value:", result)
# Stop the program
runner.stop()