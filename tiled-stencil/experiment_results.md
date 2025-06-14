# Stencil Computation Benchmark Results

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 3x3 | 1x1 | 1 | 125 | 155 |
| 10x5 | 1x1 | 1 | 127 | 157 |
| 20x20 | 1x1 | 1 | 127 | 157 |
| 6x4 | 2x1 | 1 | 132 | 162 |
| 9x9 | 3x3 | 1 | 178 | 200 |
| 9x9 | 3x3 | 2 | 363 | 419 |
| 9x9 | 3x3 | 3 | 449 | 507 |
| 6x10 | 2x4 | 1 | 174 | 205 |
| 6x10 | 2x4 | 2 | 324 | 382 |
| 12x12 | 4x5 | 1 | 256 | 151 |
| 12x12 | 4x5 | 2 | 471 | 526 |
| 12x12 | 4x5 | 3 | 625 | 679 |
| 12x12 | 4x5 | 4 | 861 | 911 |
| 14x14 | 6x6 | 1 | 363 | 244 |
| 14x14 | 6x6 | 3 | 888 | 939 |
| 14x14 | 6x6 | 6 | 1739 | 1770 |
| 20x20 | 10x10 | 1 | 782 | 558 |
| 50x50 | 10x10 | 1 | 787 | 558 |
| 100x100 | 10x10 | 1 | 787 | 558 |
| 100x100 | 20x20 | 1 | 2677 | ERROR |
| 100x100 | 20x20 | 2 | 4557 | 4572 |
| 200x200 | 20x20 | 1 | 2672 | ERROR |
| 200x200 | 20x20 | 2 | 4545 | 4571 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: Sun Jun 15 01:50:17 CEST 2025
