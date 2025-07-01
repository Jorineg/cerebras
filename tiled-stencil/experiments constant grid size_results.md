# Stencil Computation Benchmark Results for experiments constant grid size

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 18x18 | 1x1 | 1 | 127 | 156 |
| 18x18 | 2x2 | 1 | 141 | 177 |
| 18x18 | 4x4 | 1 | 220 | 131 |
| 18x18 | 8x8 | 1 | 551 | 356 |
| 32x32 | 2x2 | 1 | 141 | 178 |
| 32x32 | 3x3 | 1 | 188 | 197 |
| 32x32 | 5x5 | 1 | 285 | 191 |
| 32x32 | 10x10 | 1 | 790 | 558 |
| 34x34 | 2x2 | 2 | 271 | 339 |
| 34x34 | 3x3 | 2 | 371 | 419 |
| 34x34 | 5x5 | 2 | 596 | 635 |
| 34x34 | 10x10 | 2 | 1679 | 1712 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: Mon Jun 30 19:55:05 CEST 2025
