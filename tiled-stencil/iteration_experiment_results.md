# Stencil Iteration Benchmark Results

This document shows the cycle count for each iteration of the stencil computation for the tiled implementation.
This helps to verify that the cycle count per iteration is stable.

## Experiment: Grid 10x10, Tile 1x1, Radius 1

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 127                 | 156                 |
| 2         | 127                 | 156                 |
| 3         | 127                 | 156                 |
| 4         | 127                 | 157                 |
| 5         | 127                 | 157                 |
| 6         | 127                 | 157                 |
| 7         | 127                 | 157                 |
| 8         | 127                 | 157                 |
| 9         | 127                 | 157                 |
| 10         | 127                 | 157                 |

## Experiment: Grid 10x10, Tile 3x3, Radius 2

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 371                 | 408                 |
| 2         | 371                 | 419                 |
| 3         | 371                 | 419                 |
| 4         | 371                 | 419                 |
| 5         | 370                 | 419                 |
| 6         | 370                 | 419                 |
| 7         | 370                 | 419                 |
| 8         | 370                 | 419                 |
| 9         | 371                 | 419                 |
| 10         | 370                 | 419                 |

## Experiment: Grid 100x100, Tile 10x10, Radius 1

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 780                 | 558                 |
| 2         | 801                 | 558                 |
| 3         | 782                 | 558                 |
| 4         | 781                 | 558                 |
| 5         | 782                 | 558                 |
| 6         | 784                 | 558                 |
| 7         | 791                 | 558                 |
| 8         | 791                 | 558                 |

## Experiment: Grid 100x100, Tile 10x10, Radius 2

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 1660                 | 1700                 |
| 2         | 1679                 | 1709                 |
| 3         | 1673                 | 1716                 |
| 4         | 1689                 | 1712                 |
| 5         | 1667                 | 1711                 |
| 6         | 1672                 | 1709                 |
| 7         | 1681                 | 1712                 |
| 8         | 1676                 | 1712                 |

## Experiment: Grid 100x100, Tile 10x10, Radius 5

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
| 1         | 3332                 | 3369                 |
| 2         | 3340                 | 3379                 |
| 3         | 3333                 | 3372                 |
| 4         | 3345                 | 3378                 |
| 5         | 3355                 | 3381                 |
| 6         | 3341                 | 3380                 |
| 7         | 3373                 | 3380                 |
| 8         | 3369                 | 3378                 |

