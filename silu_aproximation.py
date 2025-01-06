import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def true_silu(x):
    return x * (1 / (1 + np.exp(-x)))

def piecewise_linear_silu(x, delta_x=0.1):
    # Create base points for interpolation
    x_base = np.arange(-30, 25 + delta_x, delta_x)
    y_base = true_silu(x_base)
    
    # Create interpolation function
    interp_func = interp1d(x_base, y_base, bounds_error=False, fill_value="extrapolate")
    
    return interp_func(x)

def evaluate_approximation(approx_func, dense_points=1000, sparse_points=200):
    # Create evaluation points
    # Dense region from -2.6 to 2.1
    x_dense = np.linspace(-2.6, 2.1, dense_points)
    
    # Sparse regions
    x_sparse_left = np.linspace(-30, -2.6, sparse_points, endpoint=False)
    x_sparse_right = np.linspace(2.1, 25, sparse_points)
    
    # Combine all points
    x_eval = np.concatenate([x_sparse_left, x_dense, x_sparse_right])
    
    # Calculate true and approximate values
    y_true = true_silu(x_eval)
    y_approx = approx_func(x_eval)
    
    # Calculate relative error
    relative_error = np.abs((y_approx - y_true) / (y_true + 1e-10))
    
    # Check if approximation meets error requirements
    dense_mask = (x_eval >= -2.6) & (x_eval <= 2.1)
    sparse_mask = ~dense_mask
    
    dense_pass = np.all(relative_error[dense_mask] < 1e-4)
    sparse_pass = np.all(relative_error[sparse_mask] < 1e-3)
    
    return x_eval, relative_error, dense_pass and sparse_pass

def plot_errors(approximations):
    plt.figure(figsize=(12, 6))
    
    # Plot error requirements
    plt.axhline(y=1e-4, color='gray', linestyle='--', alpha=0.5, label='Dense region target (1e-4)')
    plt.axhline(y=1e-3, color='gray', linestyle=':', alpha=0.5, label='Sparse region target (1e-3)')
    plt.axvline(x=-2.6, color='red', linestyle='--', alpha=0.3)
    plt.axvline(x=2.1, color='red', linestyle='--', alpha=0.3)
    
    # Plot results for each approximation
    for func, name in approximations:
        x_eval, rel_error, passes = evaluate_approximation(func)
        plt.semilogy(x_eval, rel_error, label=f'{name}')
        print(f"{name}: {'PASS' if passes else 'FAIL'}")
    
    plt.grid(True)
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('Relative Error')
    plt.title('Relative Error of SiLU Approximations')
    plt.ylim(1e-6, 1e-1)
    
    plt.show()

# Define approximations to test
approximations = [
    (lambda x: piecewise_linear_silu(x, 0.1), 'Piecewise Linear (dx=0.1)'),
]

# Run evaluation and create plot
plot_errors(approximations)
