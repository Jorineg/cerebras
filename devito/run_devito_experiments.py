import numpy as np
import time
import os
import sys
from devito import Grid, TimeFunction, Eq, Operator, clear_cache, info

# --- Core Stencil Logic ---

def execute_devito_benchmark(matrix, weights, iterations, platform='cpu'):
    """
    Creates and runs a Devito operator for the star stencil, measuring
    steady-state performance.

    This function implements the T(2N) - T(N) timing methodology.
    It runs N iterations, then runs another N iterations, and returns the
    time taken for the second set of N iterations.

    Args:
        matrix (np.ndarray): The initial data grid.
        weights (list): List of weights for the stencil.
        iterations (int): The base number of iterations (N).
        platform (str): 'cpu' or 'gpu'.

    Returns:
        float: The steady-state runtime in seconds, or -1.0 on error.
    """
    # Clear Devito's JIT cache to ensure fair compilation time for each run
    clear_cache()

    radius = len(weights) - 1
    shape = matrix.shape
    
    try:
        # 1. Define the computational grid and TimeFunction
        grid = Grid(shape=shape)
        u = TimeFunction(name='u', grid=grid, space_order=radius, time_order=1)

        # 2. Initialize the data
        u.data[0, :, :] = matrix

        # 3. Define the stencil equation symbolically
        total_weight = sum(weights) + (len(weights) - 1) * 3 * weights[0] # Correction based on previous implementation
        total_weight = weights[0] + 4 * sum(weights[1:]) # Correct total weight calculation

        weighted_sum = weights[0] * u
        for r in range(1, radius + 1):
            # Devito uses x, y, z for dimensions. For 2D, they are x and y.
            x, y = grid.dimensions
            weighted_sum += weights[r] * u.subs({x: x - r}) # Left
            weighted_sum += weights[r] * u.subs({x: x + r}) # Right
            weighted_sum += weights[r] * u.subs({y: y - r}) # Up (in matrix terms)
            weighted_sum += weights[r] * u.subs({y: y + r}) # Down (in matrix terms)

        stencil_eq = Eq(u.forward, weighted_sum / total_weight)

        # 4. Create the Operator with platform-specific settings
        op_args = {'perf_level': 'advanced'}
        if platform == 'gpu':
            op_args['platform'] = 'gpudev'
            op_args['language'] = 'cuda'
        
        op = Operator([stencil_eq], **op_args)

        # 5. Execute the benchmark using the T(2N) - T(N) method
        
        # First run for N iterations to warm up everything (JIT, cache, data on GPU)
        # We time this run to get T(N).
        start_n1 = time.time()
        # The `time_m` and `time_M` arguments run from timestep m to M-1.
        op.apply(time_m=0, time_M=iterations, dt=1)
        end_n1 = time.time()
        time_n1 = end_n1 - start_n1

        # Second run for the next N iterations. The operator resumes from the last state.
        # This measures the steady-state performance.
        start_n2 = time.time()
        op.apply(time_m=iterations, time_M=2 * iterations, dt=1)
        end_n2 = time.time()
        time_n2 = end_n2 - start_n2
        
        # The user's idea was T(2N_total) - T(N_total).
        # T(2N_total) would be time_n1 + time_n2.
        # So the calculation is (time_n1 + time_n2) - time_n1 = time_n2
        # This confirms that timing the second block of iterations is the correct approach.
        return time_n2

    except Exception as e:
        info(f"Execution failed on platform '{platform}': {e}")
        return -1.0


# --- Experiment Runner and Reporting ---

def parse_config(filename="experiments.config"):
    """Parses the configuration file."""
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        sys.exit(1)
        
    experiments = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = [int(p.strip()) for p in line.split(',')]
                experiments.append({
                    'width': parts[0],
                    'height': parts[1],
                    'radius': parts[2],
                    'iterations': parts[3]
                })
    return experiments

def generate_markdown_report(results, filename="results.md"):
    """Generates a Markdown file with the results table."""
    with open(filename, 'w') as f:
        f.write("# Stencil Benchmark Results\n\n")
        f.write("This table shows the steady-state runtime for a 2D star stencil on CPU and GPU.\n")
        f.write("Runtime is calculated as `Time(2N iterations) - Time(N iterations)` to exclude one-time setup costs.\n\n")

        # Header
        f.write("| Width | Height | Radius | Iterations (N) | CPU Time (s) | GPU Time (s) |\n")
        f.write("|---|---|---|---|---|---|\n")

        # Rows
        for res in results:
            cpu_time_str = f"{res['cpu_time']:.4f}" if res['cpu_time'] >= 0 else "Failed/Skipped"
            gpu_time_str = f"{res['gpu_time']:.4f}" if res['gpu_time'] >= 0 else "Failed/Skipped"
            
            f.write(
                f"| {res['width']} | {res['height']} | {res['radius']} | {res['iterations']} | "
                f"{cpu_time_str} | {gpu_time_str} |\n"
            )
    print(f"\nResults have been written to '{filename}'")

# --- Main Execution Block ---

if __name__ == '__main__':
    experiments = parse_config()
    all_results = []
    
    # Check for GPU availability once
    try:
        import cupy
        gpu_available = True
        info("CuPy found, GPU execution is available.")
    except ImportError:
        gpu_available = False
        info("CuPy not found. Skipping GPU benchmarks. (Install with 'pip install cupy')")

    for i, config in enumerate(experiments):
        print("-" * 50)
        print(f"Running Experiment {i+1}/{len(experiments)}: {config}")
        
        # --- Setup for the current experiment ---
        radius = config['radius']
        iterations = config['iterations']
        shape = (config['width'], config['height'])
        
        # Generate weights dynamically
        weights = [1.0 / (2**i) for i in range(radius + 1)]
        
        # Create initial data
        initial_matrix = np.random.rand(*shape).astype(np.float32)

        # --- Run on CPU ---
        print("\nRunning on CPU...")
        cpu_runtime = execute_devito_benchmark(
            initial_matrix.copy(), weights, iterations, platform='cpu'
        )
        if cpu_runtime >= 0:
            print(f"CPU steady-state time for {iterations} iterations: {cpu_runtime:.4f} s")

        # --- Run on GPU ---
        gpu_runtime = -1.0 # Default to failed state
        if gpu_available:
            print("\nRunning on GPU...")
            gpu_runtime = execute_devito_benchmark(
                initial_matrix.copy(), weights, iterations, platform='gpu'
            )
            if gpu_runtime >= 0:
                print(f"GPU steady-state time for {iterations} iterations: {gpu_runtime:.4f} s")
        else:
            print("\nSkipping GPU run (CUDA environment not available).")
            
        # --- Store results ---
        result_entry = {**config, 'cpu_time': cpu_runtime, 'gpu_time': gpu_runtime}
        all_results.append(result_entry)

    # --- Generate Final Report ---
    generate_markdown_report(all_results)