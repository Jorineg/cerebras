import numpy as np
import time
import os
import sys
import json
import subprocess

# --- Core Stencil Logic ---

def execute_devito_benchmark(matrix, weights, iterations, platform='cpu'):
    """
    Creates and runs a Devito operator for the star stencil via subprocess, measuring
    steady-state performance.

    This function uses subprocess to run the actual Devito computation with proper
    environment variables set for the specified platform.

    Args:
        matrix (np.ndarray): The initial data grid.
        weights (list): List of weights for the stencil.
        iterations (int): The base number of iterations (N).
        platform (str): 'cpu' or 'gpu'.

    Returns:
        float: The steady-state runtime in seconds, or -1.0 on error.
    """
    try:
        # Prepare configuration for the subprocess
        config = {
            'width': matrix.shape[1],
            'height': matrix.shape[0], 
            'radius': len(weights) - 1,
            'iterations': iterations
        }
        
        # Prepare environment variables
        env = os.environ.copy()
        
        if platform == 'gpu':
            env['DEVITO_PLATFORM'] = 'nvidiaX'
            # With the NVIDIA HPC SDK now installed, we can use the recommended
            # OpenACC backend with the nvc compiler.
            env['DEVITO_LANGUAGE'] = 'openacc'
            env['DEVITO_ARCH'] = 'nvc'
            
            # Prepend the NVIDIA HPC SDK compiler path to the PATH environment variable
            # This ensures that the subprocess can find the `nvc++` compiler.
            hpc_sdk_path = '/opt/nvidia/hpc_sdk/Linux_x86_64/25.5/compilers/bin'
            if os.path.isdir(hpc_sdk_path):
                env['PATH'] = f"{hpc_sdk_path}:{env.get('PATH', '')}"
            
        else:
            # Remove GPU-specific variables for CPU runs
            for var in ['DEVITO_PLATFORM', 'DEVITO_LANGUAGE', 'DEVITO_ARCH']:
                env.pop(var, None)
        
        # Run the subprocess
        result = subprocess.run(
            [sys.executable, 'run_single_experiment.py', json.dumps(config)],
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"Subprocess failed with return code {result.returncode}")
            print(f"stderr: {result.stderr}")
            print(f"stdout: {result.stdout}")
            return -1.0
        
        # Parse the runtime from stdout
        try:
            runtime = float(result.stdout.strip())
            return runtime
        except ValueError:
            print(f"Failed to parse runtime from output: '{result.stdout.strip()}'")
            print(f"stderr: {result.stderr}")
            return -1.0
            
    except subprocess.TimeoutExpired:
        print(f"Subprocess timed out after 300 seconds")
        return -1.0
    except Exception as e:
        print(f"Execution failed on platform '{platform}': {e}")
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
        print("CuPy found, GPU execution is available.")
    except ImportError:
        gpu_available = False
        print("CuPy not found. Skipping GPU benchmarks. (Install with 'pip install cupy')")

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