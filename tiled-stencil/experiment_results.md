# Stencil Computation Benchmark Results

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 3x3 | 1x1 | 1 | 125 | 155 |
| 10x5 | 1x1 | 1 | ERROR | ERROR |
| 6x4 | 2x1 | 1 | ERROR | ERROR |
| 9x9 | 3x3 | 1 | ERROR | ERROR |
| 9x9 | 3x3 | 2 | ERROR | ERROR |
| 9x9 | 3x3 | 3 | ERROR | ERROR |
| 4x8 | 2x4 | 1 | ERROR | ERROR |
| 4x8 | 2x4 | 2 | ERROR | ERROR |
| 12x12 | 4x5 | 1 | ERROR | ERROR |
| 12x12 | 4x5 | 2 | ERROR | ERROR |
| 12x12 | 4x5 | 3 | ERROR | ERROR |
| 12x12 | 4x5 | 4 | ERROR | ERROR |
| 14x14 | 6x6 | 1 | ERROR | ERROR |
| 14x14 | 6x6 | 3 | ERROR | ERROR |
| 14x14 | 6x6 | 6 | ERROR | ERROR |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: Sat Jun 14 14:45:34 CEST 2025
