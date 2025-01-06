def minimize_term():
    best_a, best_b = None, None
    min_value = float('inf')

    for a in range(1, 300):  # Suche in einem sinnvollen Bereich
        for b in range(1, 300):
            T = a * b + 16384 / b + 14336 / a + 2 * a + b
            if T < min_value:
                min_value = T
                best_a, best_b = a, b

    return best_a, best_b, min_value

a, b, minimal = minimize_term()
print(f"Optimales a: {a}, b: {b}, minimaler Term: {minimal}")
