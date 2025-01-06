width = 14336
height = 4096


def minimize_term():
    best_mx, best_nx = None, None
    min_value = float("inf")

    for mx in range(1, 300):  # Suche in einem sinnvollen Bereich
        for nx in range(1, 300):
            T = (
                mx * nx * 2 / 4
                + 10/8 * width / mx
                + nx / 2
                + min(
                    3 * height / nx / 2 + 2 * mx + 12 * mx + mx * nx / 4,
                    3 * height / nx + mx + 12 * mx + mx * nx / 4,
                    2 * height / nx + nx * height / nx * mx,
                )
            )
            if T < min_value:
                min_value = T
                best_mx, best_nx = mx, nx

    return best_mx, best_nx, min_value


mx, nx, minimal = minimize_term()
print(f"Optimales mx: {mx}, nx: {nx}, minimaler Term: {minimal}")
