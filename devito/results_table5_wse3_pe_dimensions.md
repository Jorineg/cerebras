# Stencil Benchmark Results

This table shows the steady-state runtime for a 2D star stencil on CPU and GPU.
Runtime is calculated as `Time(2N iterations) - Time(N iterations)` to exclude one-time setup costs.

| Width | Height | Radius | Iterations (N) | CPU Time (s) | GPU Time (s) |
|---|---|---|---|---|---|
| 762 | 1176 | 1 | 10000 | 1.4889 | 0.1463 |
| 762 | 1176 | 2 | 10000 | 2.5261 | 0.1467 |
| 762 | 1176 | 3 | 10000 | 3.6589 | 0.1507 |
| 762 | 1176 | 4 | 10000 | 4.6154 | 0.1621 |
| 762 | 1176 | 5 | 10000 | 6.1974 | 0.1606 |
| 762 | 1176 | 6 | 10000 | 6.9751 | 0.1733 |
| 762 | 1176 | 7 | 10000 | 8.4108 | 0.1765 |
| 762 | 1176 | 8 | 10000 | 9.3476 | 0.1820 |
| 762 | 1176 | 9 | 10000 | 10.8927 | 0.1922 |
| 762 | 1176 | 10 | 10000 | 11.8322 | 0.2000 |
