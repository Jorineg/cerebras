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
