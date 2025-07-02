# Stencil Computation Benchmark Results for experiments big compare (WSE3)

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE3 architecture.

| Grid Size | Tile Size | Radius | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|
| 260x44 | 86x14 | 1 | 5299 |
| 262x46 | 86x14 | 2 | 16696 |
| 264x48 | 86x14 | 3 | 18329 |
| 266x50 | 86x14 | 4 | 27253 |
| 268x52 | 86x14 | 5 | 33699 |
| 270x54 | 86x14 | 6 | 42772 |
| 44x29 | 14x9 | 1 | 676 |
| 46x31 | 14x9 | 2 | 1698 |
| 48x33 | 14x9 | 3 | 2703 |
| 50x35 | 14x9 | 4 | 3216 |
| 52x37 | 14x9 | 5 | 4256 |
| 54x39 | 14x9 | 6 | 4732 |
| 44x5 | 14x1 | 1 | 243 |
| 46x7 | 14x2 | 2 | 747 |
| 48x9 | 14x3 | 3 | 1168 |
| 50x11 | 14x4 | 4 | 1848 |
| 52x13 | 14x5 | 5 | 2635 |
| 54x15 | 14x6 | 6 | 3652 |
| 8x5 | 2x1 | 1 | 162 |
| 10x10 | 2x2 | 2 | 339 |
| 15x15 | 3x3 | 3 | 526 |
| 20x20 | 4x4 | 4 | 808 |
| 25x25 | 5x5 | 5 | 1389 |
| 30x30 | 6x6 | 6 | 1879 |
| 5x5 | 1x1 | 1 | 157 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Architecture: wse3
- Generated on: Tue Jul  1 21:50:29 CEST 2025
