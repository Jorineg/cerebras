# Stencil Computation Benchmark Results Comparison (WSE2 vs WSE3)

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values comparing WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 260x44 | 86x14 | 1 | 7741 | 5299 |
| 262x46 | 86x14 | 2 | 16678 | 16696 |
| 264x48 | 86x14 | 3 | 18305 | 18329 |
| 266x50 | 86x14 | 4 | 27168 | 27253 |
| 268x52 | 86x14 | 5 | 33304 | 33699 |
| 270x54 | 86x14 | 6 | 42663 | 42772 |
| 44x29 | 14x9 | 1 | 841 | 676 |
| 46x31 | 14x9 | 2 | 1656 | 1698 |
| 48x33 | 14x9 | 3 | 2672 | 2703 |
| 50x35 | 14x9 | 4 | 3190 | 3216 |
| 52x37 | 14x9 | 5 | 4194 | 4256 |
| 54x39 | 14x9 | 6 | 4753 | 4732 |
| 44x5 | 14x1 | 1 | 232 | 243 |
| 46x7 | 14x2 | 2 | 705 | 747 |
| 48x9 | 14x3 | 3 | 1118 | 1168 |
| 50x11 | 14x4 | 4 | 1809 | 1848 |
| 52x13 | 14x5 | 5 | 2612 | 2635 |
| 54x15 | 14x6 | 6 | 3643 | 3652 |
| 8x5 | 2x1 | 1 | 131 | 162 |
| 10x10 | 2x2 | 2 | 271 | 339 |
| 15x15 | 3x3 | 3 | 450 | 526 |
| 20x20 | 4x4 | 4 | 775 | 808 |
| 25x25 | 5x5 | 5 | 1364 | 1389 |
| 30x30 | 6x6 | 6 | 1859 | 1879 |
| 5x5 | 1x1 | 1 | 127 | 157 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- WSE2 vs WSE3 architecture comparison
- Generated on: Tue Jul  1 21:50:29 CEST 2025
