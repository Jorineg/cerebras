#!/usr/bin/env python3
"""
Single experiment runner for Devito benchmarks.
This script is designed to be called as a subprocess with specific environment variables.
"""

import numpy as np
import time
import sys
import json
import traceback
from devito import Grid, TimeFunction, Eq, Operator, clear_cache, info

def execute_devito_benchmark(matrix, weights, iterations):
    """
    Creates and runs a Devito operator for the star stencil, measuring
    steady-state performance.
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
        # This manual definition is restored to allow variable radius sizes.
        total_weight = weights[0] + 4 * sum(weights[1:])

        weighted_sum = weights[0] * u
        for r in range(1, radius + 1):
            # Using .shift() is the robust, symbolic way for GPU compatibility
            weighted_sum += weights[r] * u.shift(u.dimensions[-2], -r) # Left
            weighted_sum += weights[r] * u.shift(u.dimensions[-2], r)  # Right
            weighted_sum += weights[r] * u.shift(u.dimensions[-1], -r) # Up
            weighted_sum += weights[r] * u.shift(u.dimensions[-1], r)  # Down

        stencil_eq = Eq(u.forward, weighted_sum / total_weight)

        # 4. Create the Operator
        op = Operator([stencil_eq])

        # 5. Execute the benchmark using the T(2N) - T(N) method
        
        # First run for N iterations to warm up everything (JIT, cache, data on GPU)
        start_n1 = time.time()
        op.apply(time_m=0, time_M=iterations, dt=1)
        end_n1 = time.time()
        time_n1 = end_n1 - start_n1

        # Second run for the next N iterations. The operator resumes from the last state.
        start_n2 = time.time()
        op.apply(time_m=iterations, time_M=2 * iterations, dt=1)
        end_n2 = time.time()
        time_n2 = end_n2 - start_n2
        
        return time_n2

    except Exception as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return -1.0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run_single_experiment.py <config_json>", file=sys.stderr)
        sys.exit(1)
    
    # Parse configuration from command line
    config = json.loads(sys.argv[1])
    
    # Extract parameters
    width = config['width']
    height = config['height']
    radius = config['radius']
    iterations = config['iterations']
    
    # Generate weights dynamically
    weights = [1.0 / (2**i) for i in range(radius + 1)]
    
    # Create initial data
    shape = (width, height)
    initial_matrix = np.random.rand(*shape).astype(np.float32)
    
    # Run the benchmark
    runtime = execute_devito_benchmark(initial_matrix, weights, iterations)
    
    # Output the result
    print(runtime) 