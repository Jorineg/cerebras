import numpy as np


def star_stencil(matrix, weights, iterations):
    """
    Applies a star-shaped stencil for weighted averaging on a matrix.
    """
    matrix = np.array(matrix, dtype=float)
    radius = len(weights) - 1
    rows, cols = matrix.shape

    for iter in range(iterations):
        new_matrix = matrix.copy()

        # Only update non-border elements
        for i in range(radius, rows - radius):
            for j in range(radius, cols - radius):
                weighted_sum = matrix[i, j] * weights[0]  # Center point
                total_weight = weights[0]

                # Apply stencil for each distance level
                for r in range(1, radius + 1):
                    # Up, Down, Left, Right
                    neighbors = [
                        matrix[i - r, j],  # Up
                        matrix[i + r, j],  # Down
                        matrix[i, j - r],  # Left
                        matrix[i, j + r],  # Right
                    ]
                    weighted_sum += sum(neighbors) * weights[r]
                    total_weight += 4 * weights[r]

                new_matrix[i, j] = weighted_sum / total_weight

        matrix = new_matrix

    return matrix


# Function to print matrix nicely
def print_matrix(matrix, title="Matrix"):
    print(f"\n{title}:")
    with np.printoptions(precision=1, suppress=True, linewidth=100):
        print(matrix)


if __name__ == "__main__":

    # Create a small test matrix
    # toy_matrix = np.array(
    #     [
    #         [1, 1, 1, 1, 1],
    #         [1, 2, 2, 2, 1],
    #         [1, 2, 5, 2, 1],
    #         [1, 2, 2, 2, 1],
    #         [1, 1, 1, 1, 1],
    #     ],
    #     dtype=np.float32,
    # )

    toy_matrix = np.array(
        [
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18],
            [19, 20, 21, 22, 23, 0],
            [25, 26, 27, 28, 29, 30],
            [31, 32, 33, 34, 35, 36],
        ],
        dtype=np.float32,
    )

    # Test the function
    weights = [1.0, 0.5, 0.25]  # Center weight and neighbor weight
    iterations = 100

    print_matrix(toy_matrix, "Original Matrix")
    result = star_stencil(toy_matrix, weights, iterations)
    print_matrix(result, "Result after stencil operation")
    print_matrix(result - toy_matrix, "Difference (Result - Original)")
