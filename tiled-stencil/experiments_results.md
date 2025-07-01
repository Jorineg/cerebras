# Stencil Computation Benchmark Results for experiments

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 3x3 | 1x1 | 1 | 125 | 155 |
| 10x5 | 1x1 | 1 | 126 | 156 |
| 20x20 | 1x1 | 1 | 127 | 156 |
| 6x4 | 2x1 | 1 | 131 | 162 |
| 9x9 | 3x3 | 1 | 188 | 197 |
| 9x9 | 3x3 | 2 | 371 | 419 |
| 9x9 | 3x3 | 3 | 444 | 526 |
| 6x10 | 2x4 | 1 | 174 | 204 |
| 6x10 | 2x4 | 2 | 323 | 382 |
| 12x12 | 4x5 | 1 | 240 | 150 |
| 12x12 | 4x5 | 2 | 477 | 527 |
| 12x12 | 4x5 | 3 | 693 | 740 |
| 12x12 | 4x5 | 4 | 839 | 872 |
| 14x14 | 6x6 | 1 | 338 | 244 |
| 14x14 | 6x6 | 3 | 894 | 939 |
| 14x14 | 6x6 | 6 | 1872 | 1879 |
| 20x20 | 10x10 | 1 | 783 | 558 |
| 50x50 | 10x10 | 1 | 785 | 558 |
| 100x100 | 10x10 | 1 | 781 | 558 |
| 100x100 | 20x20 | 1 | 2669 | 1788 |
| 100x100 | 20x20 | 2 | 4548 | 4570 |
| 200x200 | 20x20 | 1 | 2672 | 1788 |
| 200x200 | 20x20 | 2 | 4541 | 4566 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: Mon Jun 30 11:55:43 CEST 2025
