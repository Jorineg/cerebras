# Stencil Iteration Benchmark Results

This document shows the cycle count for each iteration of the stencil computation for the r1 implementation.
This helps to verify that the cycle count per iteration is stable.

## Experiment: Grid 3x3, Radius 1

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 8                 | 10                 |
| 2         | 15                 | 24                 |
| 3         | 12                 | 17                 |
| 4         | 12                 | 17                 |
| 5         | 12                 | 17                 |
| 6         | 12                 | 17                 |
| 7         | 12                 | 17                 |
| 8         | 14                 | 17                 |
| 9         | 12                 | 17                 |
| 10         | 12                 | 17                 |

## Experiment: Grid 10x10, Radius 1

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 8                 | 1                 |
| 2         | 14                 | 23                 |
| 3         | 16                 | 24                 |
| 4         | 16                 | 23                 |
| 5         | 17                 | 23                 |
| 6         | 16                 | 23                 |
| 7         | 17                 | 23                 |
| 8         | 15                 | 23                 |

