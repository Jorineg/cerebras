#!/bin/bash

# Check if correct number of arguments provided
if [ $# -ne 5 ]; then
    echo "Usage: $0 <width> <height> <tile_width> <tile_height> <radius>"
    exit 1
fi

WIDTH=$1
HEIGHT=$2
TILE_WIDTH=$3
TILE_HEIGHT=$4
RADIUS=$5

export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace

# Function to run benchmark for a specific architecture
run_benchmark() {
    local ARCH=$1
    local ITERATIONS_LOW=4
    local ITERATIONS_HIGH=8
    
    # Compile for this architecture
    NUM_PE_X=$(((WIDTH - 2 * RADIUS) / TILE_WIDTH + 2))
    NUM_PE_Y=$(((HEIGHT - 2 * RADIUS) / TILE_HEIGHT + 2))
    
    cslc layout.csl \
    --fabric-dims=$((NUM_PE_X+7)),$((NUM_PE_Y+2)) \
    --fabric-offsets=4,1 \
    --params=w:$WIDTH,h:$HEIGHT,tile_width:$TILE_WIDTH,tile_height:$TILE_HEIGHT,radius:$RADIUS \
    --memcpy \
    --channels=1 \
    --arch=$ARCH \
    --link-section-start-address-bytes=".own_values:20960,.buffer:40960" \
    -o out_$ARCH > /dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        echo -1
        return
    fi
    
    # Run with low iterations
    cs_python run.py --name out_$ARCH --num-iterations $ITERATIONS_LOW > /dev/null 2>&1
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
    
    # Run with high iterations
    cs_python run.py --name out_$ARCH --num-iterations $ITERATIONS_HIGH > /dev/null 2>&1
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

# Adjust width and height to be multiples of tile dimensions
INNER_W=$((WIDTH - 2 * RADIUS))
INNER_H=$((HEIGHT - 2 * RADIUS))

REMAINDER_W=$((INNER_W % TILE_WIDTH))
REMAINDER_H=$((INNER_H % TILE_HEIGHT))

if [ $REMAINDER_W -ne 0 ]; then
    PAD_W=$((TILE_WIDTH - REMAINDER_W))
    WIDTH=$((WIDTH + PAD_W))
fi

if [ $REMAINDER_H -ne 0 ]; then
    PAD_H=$((TILE_HEIGHT - REMAINDER_H))
    HEIGHT=$((HEIGHT + PAD_H))
fi

# Run benchmarks for both architectures
wse2_cycles=$(run_benchmark "wse2")
wse3_cycles=$(run_benchmark "wse3")

# Output results
echo "$wse2_cycles $wse3_cycles"

# Cleanup
rm -f out_wse2* out_wse3* python.log 2>/dev/null 