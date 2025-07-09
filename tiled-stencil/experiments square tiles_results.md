# Stencil Computation Benchmark Results for experiments square tiles (WSE3)

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE3 architecture.

| Grid Size | Tile Size | Radius | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|
| 5x5 | 1x1 | 1 | 157 |
| 8x8 | 2x2 | 1 | 177 |
| 10x10 | 2x2 | 2 | 339 |
| 11x11 | 3x3 | 1 | 197 |
| 13x13 | 3x3 | 2 | 419 |
| 14x14 | 4x4 | 1 | 131 |
| 16x16 | 4x4 | 2 | 478 |
| 20x20 | 4x4 | 4 | 808 |
| 17x17 | 5x5 | 1 | 191 |
| 19x19 | 5x5 | 2 | 635 |
| 23x23 | 5x5 | 4 | 1036 |
| 23x23 | 7x7 | 1 | 297 |
| 25x25 | 7x7 | 2 | 1003 |
| 29x29 | 7x7 | 4 | 1875 |
| 33x33 | 7x7 | 6 | 2645 |
| 32x32 | 10x10 | 1 | 558 |
| 34x34 | 10x10 | 2 | 1712 |
| 38x38 | 10x10 | 4 | 2747 |
| 42x42 | 10x10 | 6 | 4179 |
| 47x47 | 15x15 | 1 | 1078 |
| 49x49 | 15x15 | 2 | 3418 |
| 53x53 | 15x15 | 4 | 6879 |
| 57x57 | 15x15 | 6 | 9890 |
| 62x62 | 20x20 | 1 | 1788 |
| 64x64 | 20x20 | 2 | 4572 |
| 68x68 | 20x20 | 4 | 9754 |
| 72x72 | 20x20 | 6 | 13355 |
| 77x77 | 25x25 | 1 | 2852 |
| 79x79 | 25x25 | 2 | 8149 |
| 83x83 | 25x25 | 4 | 14870 |
| 87x87 | 25x25 | 6 | 22865 |
| 92x92 | 30x30 | 1 | 3988 |
| 94x94 | 30x30 | 2 | 12431 |
| 98x98 | 30x30 | 4 | 20182 |
| 102x102 | 30x30 | 6 | 31526 |
| 122x122 | 40x40 | 1 | 6748 |
| 124x124 | 40x40 | 2 | 16880 |
| 128x128 | 40x40 | 4 | 36805 |
| 132x132 | 40x40 | 6 | 50378 |
| 152x152 | 50x50 | 1 | 10627 |
| 154x154 | 50x50 | 2 | 33546 |
| 158x158 | 50x50 | 4 | 54425 |
| 162x162 | 50x50 | 6 | 85330 |
| 182x182 | 60x60 | 1 | 14907 |
| 184x184 | 60x60 | 2 | 37207 |
| 188x188 | 60x60 | 4 | 81445 |
| 192x192 | 60x60 | 6 | 111297 |
| 192x192 | 64x64 | 1 | 16924 |
| 194x194 | 64x64 | 2 | 42228 |
| 198x198 | 64x64 | 4 | 92532 |
| 202x202 | 64x64 | 6 | ERROR |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Architecture: wse3
- Generated on: Thu Jul 10 00:28:57 CEST 2025
