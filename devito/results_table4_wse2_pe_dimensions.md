# Stencil Benchmark Results

This table shows the steady-state runtime for a 2D star stencil on CPU and GPU.
Runtime is calculated as `Time(2N iterations) - Time(N iterations)` to exclude one-time setup costs.

| Width | Height | Radius | Iterations (N) | CPU Time (s) | GPU Time (s) |
|---|---|---|---|---|---|
| 750 | 994 | 1 | 10000 | 1.2376 | 0.1358 |
| 750 | 994 | 2 | 10000 | 2.1257 | 0.1383 |
| 750 | 994 | 3 | 10000 | 3.2082 | 0.1419 |
| 750 | 994 | 4 | 10000 | 3.9705 | 0.1449 |
| 750 | 994 | 5 | 10000 | 5.0418 | 0.1497 |
| 750 | 994 | 6 | 10000 | 5.7826 | 0.1554 |
| 750 | 994 | 7 | 10000 | 7.0630 | 0.1625 |
| 750 | 994 | 8 | 10000 | 7.8751 | 0.1691 |
| 750 | 994 | 9 | 10000 | 9.1778 | 0.1771 |
| 750 | 994 | 10 | 10000 | 9.9529 | 0.1836 |
