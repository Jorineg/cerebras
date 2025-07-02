# Stencil Computation Benchmark Results for experiments gpu compare

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
| 56x4 | 14x1 | 1 | 232 | 243 |
| 44x8 | 11x2 | 1 | 279 | 283 |
| 56x8 | 14x2 | 2 | 705 | 747 |
| 44x8 | 11x2 | 2 | 596 | 644 |
| 56x12 | 14x3 | 3 | 1124 | 1168 |
| 44x12 | 11x3 | 3 | 1001 | 1054 |
| 56x16 | 14x4 | 4 | 1803 | 1848 |
| 44x16 | 11x4 | 4 | 1714 | 1756 |
| 56x20 | 14x5 | 5 | 2594 | 2634 |
| 44x20 | 11x5 | 5 | 2195 | 2232 |
| 56x24 | 14x6 | 6 | 3619 | 3653 |
| 44x24 | 11x6 | 6 | 3370 | 3379 |

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: Tue Jul  1 20:11:53 CEST 2025
