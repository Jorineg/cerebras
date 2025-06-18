#!/bin/bash

# Hardcoded experiment configurations
# Format: width,height,tile_width,tile_height,radius,max_iterations
EXPERIMENTS=(
    "10,10,1,1,1,10"
    "10,10,3,3,2,10"
    "100,100,10,10,1,8"
    "100,100,10,10,2,8"
    "100,100,10,10,5,8"
)

RESULTS_FILE="iteration_experiment_results.md"


export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace


# Initialize results file
cat > "$RESULTS_FILE" << EOF
# Stencil Iteration Benchmark Results

This document shows the cycle count for each iteration of the stencil computation for the tiled implementation.
This helps to verify that the cycle count per iteration is stable.

EOF

# Main loop for experiments
for exp in "${EXPERIMENTS[@]}"; do
    IFS=',' read -r width height tile_width tile_height radius max_iterations <<< "$exp"

    echo "Running experiment: Grid ${width}x${height}, Tile ${tile_width}x${tile_height}, Radius ${radius}, Max Iterations ${max_iterations}"

    # Write experiment header to results file
    cat >> "$RESULTS_FILE" << EOF
## Experiment: Grid ${width}x${height}, Tile ${tile_width}x${tile_height}, Radius ${radius}

| Iteration | WSE2 Cycles for Iteration | WSE3 Cycles for Iteration |
|-----------|---------------------------|---------------------------|
EOF

    # Pad width and height to be multiples of tile dimensions
    padded_width=$width
    padded_height=$height
    inner_w=$((padded_width - 2 * radius))
    inner_h=$((padded_height - 2 * radius))
    remainder_w=$((inner_w % tile_width))
    remainder_h=$((inner_h % tile_height))

    if [ $remainder_w -ne 0 ]; then
        padded_width=$((padded_width + tile_width - remainder_w))
    fi
    if [ $remainder_h -ne 0 ]; then
        padded_height=$((padded_height + tile_height - remainder_h))
    fi
    
    num_pe_x=$(((padded_width - 2 * radius) / tile_width + 2))
    num_pe_y=$(((padded_height - 2 * radius) / tile_height + 2))

    # Compile for WSE2
    echo "  Compiling for WSE2..."
    cslc layout.csl \
        --fabric-dims=$((num_pe_x+7)),$((num_pe_y+2)) \
        --fabric-offsets=4,1 \
        --params=w:$padded_width,h:$padded_height,tile_width:$tile_width,tile_height:$tile_height,radius:$radius \
        --memcpy \
        --channels=1 \
        --arch=wse2 \
        --max-inlined-iterations=1000000 \
        -o out_wse2 > cslc_wse2.log 2>&1
    if [ $? -ne 0 ]; then
        echo "    WSE2 compilation failed. See cslc_wse2.log"
        wse2_compile_failed=true
    else
        wse2_compile_failed=false
    fi

    # Compile for WSE3
    echo "  Compiling for WSE3..."
    cslc layout.csl \
        --fabric-dims=$((num_pe_x+7)),$((num_pe_y+2)) \
        --fabric-offsets=4,1 \
        --params=w:$padded_width,h:$padded_height,tile_width:$tile_width,tile_height:$tile_height,radius:$radius \
        --memcpy \
        --channels=1 \
        --arch=wse3 \
        --max-inlined-iterations=1000000 \
        -o out_wse3 > cslc_wse3.log 2>&1
    if [ $? -ne 0 ]; then
        echo "    WSE3 compilation failed. See cslc_wse3.log"
        wse3_compile_failed=true
    else
        wse3_compile_failed=false
    fi

    wse2_cycles=()
    wse3_cycles=()

    # Run for 0 to max_iterations
    for i in $(seq 0 $max_iterations); do
        echo "    Running for $i iterations..."
        
        # WSE2
        if [ "$wse2_compile_failed" = true ]; then
            wse2_total_cycles=-1
        else
            cs_python run.py --name out_wse2 --num-iterations $i > python.log 2>&1
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
        echo "wse2_total_cycles: $wse2_total_cycles"
        wse2_cycles+=($wse2_total_cycles)

        # WSE3
        if [ "$wse3_compile_failed" = true ]; then
            wse3_total_cycles=-1
        else
            cs_python run.py --name out_wse3 --num-iterations $i > python.log 2>&1
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
        echo "wse3_total_cycles: $wse3_total_cycles"
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
echo "Tiled stencil iteration experiments finished."
echo "Results saved to $RESULTS_FILE"
echo
echo "=== Results Preview ==="
cat "$RESULTS_FILE" 