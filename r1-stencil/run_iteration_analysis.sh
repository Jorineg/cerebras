#!/bin/bash

# Hardcoded experiment configurations
# Format: width,height,radius,max_iterations
EXPERIMENTS=(
    "3,3,1,10"
    "10,10,1,8"
)

RESULTS_FILE="iteration_experiment_results.md"

export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace


# Initialize results file
cat > "$RESULTS_FILE" << EOF
# Stencil Iteration Benchmark Results

This document shows the cycle count for each iteration of the stencil computation for the r1 implementation.
This helps to verify that the cycle count per iteration is stable.

EOF

# Main loop for experiments
for exp in "${EXPERIMENTS[@]}"; do
    IFS=',' read -r width height radius max_iterations <<< "$exp"

    echo "Running experiment: Grid ${width}x${height}, Radius ${radius}, Max Iterations ${max_iterations}"

    # Write experiment header to results file
    cat >> "$RESULTS_FILE" << EOF
## Experiment: Grid ${width}x${height}, Radius ${radius}

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
EOF

    wse2_cycles=()
    wse3_cycles=()

    num_pe_x=$((width - 2 * radius + 2))
    num_pe_y=$((height - 2 * radius + 2))

    # Run for 0 to max_iterations
    for i in $(seq 0 $max_iterations); do
        echo "    Running for $i iterations..."
        
        # WSE2
        echo "      Compiling and running for WSE2..."
        cslc layout.csl \
            --fabric-dims=$((num_pe_x+7)),$((num_pe_y+2)) \
            --fabric-offsets=4,1 \
            --params=w:$width,h:$height,steps:$i \
            --arch=wse2 \
            --memcpy \
            --channels=1 \
            -o out_wse2 > cslc_wse2.log 2>&1
        
        if [ $? -ne 0 ]; then
            wse2_total_cycles=-1
        else
            cs_python run.py --name out_wse2 > python.log 2>&1
            if [ $? -ne 0 ]; then
                wse2_total_cycles=-1
            else
                python3 filter_traces.py <<EOF > /dev/null
5
2
EOF
                wse2_total_cycles=$(python3 get_cycles.py 2>/dev/null)
                if ! [[ "$wse2_total_cycles" =~ ^[0-9]+$ ]]; then
                    wse2_total_cycles=-1
                fi
            fi
        fi
        wse2_cycles+=($wse2_total_cycles)

        # WSE3
        echo "      Compiling and running for WSE3..."
        cslc layout.csl \
            --fabric-dims=$((num_pe_x+7)),$((num_pe_y+2)) \
            --fabric-offsets=4,1 \
            --params=w:$width,h:$height,steps:$i \
            --arch=wse3 \
            --memcpy \
            --channels=1 \
            -o out_wse3 > cslc_wse3.log 2>&1
        
        if [ $? -ne 0 ]; then
            wse3_total_cycles=-1
        else
            cs_python run.py --name out_wse3 > python.log 2>&1
            if [ $? -ne 0 ]; then
                wse3_total_cycles=-1
            else
                python3 filter_traces.py <<EOF > /dev/null
5
2
EOF
                wse3_total_cycles=$(python3 get_cycles.py 2>/dev/null)
                if ! [[ "$wse3_total_cycles" =~ ^[0-9]+$ ]]; then
                    wse3_total_cycles=-1
                fi
            fi
        fi
        wse3_cycles+=($wse3_total_cycles)
    done

    # Calculate and write per-iteration cycles
    for i in $(seq 1 $max_iterations); do
        prev_i=$((i-1))
        
        # WSE2
        if [ "${wse2_cycles[$i]}" = "-1" ] || [ "${wse2_cycles[$prev_i]}" = "-1" ]; then
            wse2_iter_cycles="ERROR"
        else
            wse2_iter_cycles=$((wse2_cycles[$i] - wse2_cycles[$prev_i]))
        fi

        # WSE3
        if [ "${wse3_cycles[$i]}" = "-1" ] || [ "${wse3_cycles[$prev_i]}" = "-1" ]; then
            wse3_iter_cycles="ERROR"
        else
            wse3_iter_cycles=$((wse3_cycles[$i] - wse3_cycles[$prev_i]))
        fi
        
        echo "| $i         | $wse2_iter_cycles                 | $wse3_iter_cycles                 |" >> "$RESULTS_FILE"
    done

    echo "" >> "$RESULTS_FILE"
done

echo
echo "R1 stencil iteration experiments finished."
echo "Results saved to $RESULTS_FILE"
echo
echo "=== Results Preview ==="
cat "$RESULTS_FILE" 