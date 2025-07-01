#!/bin/bash

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <width> <height>"
    exit 1
fi

WIDTH=$1
HEIGHT=$2

export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace

# Function to run benchmark for a specific architecture
run_benchmark() {
    local ARCH=$1
    local ITERATIONS_LOW=2
    local ITERATIONS_HIGH=4
    
    # Compile for this architecture
    
    cslc layout.csl \
    --fabric-dims=$((WIDTH+7)),$((HEIGHT+2)) \
    --fabric-offsets=4,1 \
    --params=w:$WIDTH,h:$HEIGHT,steps:$ITERATIONS_LOW \
    --memcpy \
    --channels=1 \
    --arch=$ARCH \
    --max-inlined-iterations=1000000 \
    -o out_$ARCH > /dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        echo -1
        return
    fi
    
    # Run with low iterations
    cs_python run.py --name out_$ARCH > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -1
        return
    fi
    
    python3 filter_traces.py > /dev/null 2>&1 <<EOF
5
2
EOF
    
    cycles_low=$(python3 get_cycles.py 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$cycles_low" ]; then
        echo -1
        return
    fi

    # compile for high iterations
    cslc layout.csl \
    --fabric-dims=$((WIDTH+7)),$((HEIGHT+2)) \
    --fabric-offsets=4,1 \
    --params=w:$WIDTH,h:$HEIGHT,steps:$ITERATIONS_HIGH \
    --memcpy \
    --channels=1 \
    --arch=$ARCH \
    --max-inlined-iterations=1000000 \
    -o out_$ARCH > /dev/null 2>&1
    
    # Run with high iterations
    cs_python run.py --name out_$ARCH > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -1
        return
    fi
    
    python3 filter_traces.py > /dev/null 2>&1 <<EOF
5
2
EOF
    
    cycles_high=$(python3 get_cycles.py 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$cycles_high" ]; then
        echo -1
        return
    fi
    
    # Calculate average cycles per iteration
    cycles_diff=$((cycles_high - cycles_low))
    avg_cycles_per_iter=$((cycles_diff / (ITERATIONS_HIGH - ITERATIONS_LOW)))
    
    echo $avg_cycles_per_iter
}

# Run benchmarks for both architectures
wse2_cycles=$(run_benchmark "wse2")
wse3_cycles=$(run_benchmark "wse3")

# Output results
echo "$wse2_cycles $wse3_cycles"

# Cleanup
rm -f out_wse2* out_wse3* python.log 2>/dev/null 