# Stencil Benchmark Results

This table shows the steady-state runtime for a 2D star stencil on CPU and GPU.
Runtime is calculated as `Time(2N iterations) - Time(N iterations)` to exclude one-time setup costs.

| Width | Height | Radius | Iterations (N) | CPU Time (s) | GPU Time (s) |
|---|---|---|---|---|---|
| 100 | 100 | 1 | 1000000 | 2.2112 | 9.7309 |
| 100 | 100 | 2 | 1000000 | 3.8160 | 9.7270 |
| 100 | 100 | 3 | 1000000 | 5.5279 | 9.7356 |
| 100 | 100 | 4 | 1000000 | 6.5409 | 9.7659 |
| 100 | 100 | 5 | 1000000 | 8.4157 | 9.7529 |
| 100 | 100 | 6 | 1000000 | 9.9961 | 9.7708 |
| 100 | 1000 | 1 | 100000 | 2.2146 | 1.0429 |
| 100 | 1000 | 2 | 100000 | 4.0623 | 1.0466 |
| 100 | 1000 | 3 | 100000 | 5.3653 | 1.0331 |
| 100 | 1000 | 4 | 100000 | 6.5379 | 1.0302 |
| 100 | 1000 | 5 | 100000 | 8.4115 | 1.0409 |
| 100 | 1000 | 6 | 100000 | 10.0371 | 1.0582 |
| 1000 | 1000 | 1 | 10000 | 1.6103 | 0.1487 |
| 1000 | 1000 | 2 | 10000 | 2.8188 | 0.1526 |
| 1000 | 1000 | 3 | 10000 | 4.4377 | 0.1582 |
| 1000 | 1000 | 4 | 10000 | 6.0163 | 0.1584 |
| 1000 | 1000 | 5 | 10000 | 7.9296 | 0.1669 |
| 1000 | 1000 | 6 | 10000 | 10.0127 | 0.1734 |
| 1000 | 10000 | 1 | 1000 | 2.6174 | 0.0761 |
| 1000 | 10000 | 2 | 1000 | 4.1815 | 0.0791 |
| 1000 | 10000 | 3 | 1000 | 5.5225 | 0.0833 |
| 1000 | 10000 | 4 | 1000 | 6.3532 | 0.0839 |
| 1000 | 10000 | 5 | 1000 | 8.3064 | 0.0955 |
| 1000 | 10000 | 6 | 1000 | 10.0940 | 0.1000 |
| 10000 | 10000 | 1 | 100 | 3.6835 | 0.1800 |
| 10000 | 10000 | 2 | 100 | 4.5234 | 0.1896 |
| 10000 | 10000 | 3 | 100 | 5.8971 | 0.1336 |
| 10000 | 10000 | 4 | 100 | 6.6253 | 0.1874 |
| 10000 | 10000 | 5 | 100 | 7.5088 | 0.1867 |
| 10000 | 10000 | 6 | 100 | 8.6515 | 0.1481 |
| 100000 | 10000 | 1 | 10 | 2.9368 | 0.7380 |
| 100000 | 10000 | 2 | 10 | 4.1719 | 0.7398 |
| 100000 | 10000 | 3 | 10 | 5.3896 | 0.7418 |
| 100000 | 10000 | 4 | 10 | 6.6300 | 0.7474 |
| 100000 | 10000 | 5 | 10 | 7.5125 | 0.7580 |
| 100000 | 10000 | 6 | 10 | 8.8995 | 0.7600 |
| 100000 | 100000 | 1 | 1 | 7.3616 | Failed/Skipped |
| 100000 | 100000 | 2 | 1 | 7.6407 | Failed/Skipped |
| 100000 | 100000 | 3 | 1 | 14.2644 | Failed/Skipped |
| 100000 | 100000 | 4 | 1 | Failed/Skipped | Failed/Skipped |
| 100000 | 100000 | 5 | 1 | Failed/Skipped | Failed/Skipped |
| 100000 | 100000 | 6 | 1 | Failed/Skipped | Failed/Skipped |

## Notes

- Experiments 1-36 completed successfully on both CPU and GPU
- Experiments 37-39 completed on CPU but failed on GPU with CUDA errors (CUDA_ERROR_INVALID_VALUE)
- Experiments 40-42 were interrupted during execution
- GPU failures for large arrays (100000x100000) suggest memory allocation issues or kernel launch parameter problems
- The run was manually canceled during experiment 40 CPU execution 