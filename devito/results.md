# Stencil Benchmark Results

This table shows the steady-state runtime for a 2D star stencil on CPU and GPU.
Runtime is calculated as `Time(2N iterations) - Time(N iterations)` to exclude one-time setup costs.

| Width | Height | Radius | Iterations (N) | CPU Time (s) | GPU Time (s) |
|---|---|---|---|---|---|
| 512 | 512 | 2 | 100 | 0.0061 | 0.0107 |
| 100 | 100 | 1 | 1000000 | 1.6687 | 38.1491 |
| 100 | 100 | 2 | 1000000 | 2.6944 | 39.9370 |
| 1000 | 1000 | 1 | 10000 | 2.0427 | 0.6289 |
| 1000 | 1000 | 2 | 10000 | 2.5445 | 0.6861 |
| 10000 | 10000 | 1 | 100 | 5.1794 | 0.7456 |
| 10000 | 10000 | 2 | 100 | 5.6843 | 0.7806 |
| 512 | 512 | 2 | 100 | 0.0076 | 0.0060 |
| 1024 | 1024 | 2 | 100 | 0.0345 | 0.0109 |
| 2048 | 2048 | 4 | 50 | 0.1528 | 0.0303 |
| 4096 | 4096 | 4 | 50 | 0.6311 | 0.0844 |


---

## System Configuration

**Generated:** 2025-07-01 16:50:20

### CPU Information
- **Processor:** 13th Gen Intel(R) Core(TM) i7-13700H
- **Architecture:** x86_64
- **Sockets:** 1
- **Cores per Socket:** 2
- **Threads per Core:** 2
- **Logical CPUs:** 4
- **Current Frequency:** 2918.414 MHz
- **NUMA Nodes:** 1
- **Key Features:** avx, avx2, sse4, fma
- **Cache:** L1D: 96 KiB (2 instances), L1I: 64 KiB (2 instances), L2: 2.5 MiB (2 instances), L3: 24 MiB (1 instance)

### Memory Information
- **Total RAM:** 15.62 GB
- **Available RAM:** 14.47 GB
- **Swap:** 0.0 GB

### GPU Information
- **GPU 1:** NVIDIA GeForce RTX 4050 Laptop GPU
  - **Memory:** 6141 MB
  - **Compute Capability:** 8.9
  - **Driver Version:** 576.40
  - **PCI Bus ID:** 00000000:01:00.0
  - **Max Power:** 45.00 W
  - **Max Graphics Clock:** 3105 MHz
  - **Max Memory Clock:** 8001 MHz
- **CUDA Version:** Cuda compilation tools, release 12.0, V12.0.140

### System Information
- **OS:** Ubuntu 24.04.1 LTS
- **Kernel:** 6.6.87.2-microsoft-standard-WSL2
- **Hostname:** Jorin
- **Uptime:** 16:50:19 up  3:43,  1 user,  load average: 0.46, 0.15, 0.05
- **Root Disk Usage:** /dev/sdc       1007G   47G  909G   5% /

### Software Versions
- **Python:** 3.12.3

#### Scientific Libraries
- **NUMPY:** 2.2.6
- **DEVITO:** 4.8.18
- **CUPY:** 13.4.1
- **SYMPY:** 1.14.0

#### Compilers
- **GCC:** gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
- **G++:** g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
- **NVC:** 

#### Build Tools
- **CMAKE:** 
- **MAKE:** GNU Make 4.3
- **CuPy CUDA Runtime:** CUDA 12.8
