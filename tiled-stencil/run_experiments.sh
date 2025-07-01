#!/bin/bash

# Check if experiment config file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <experiment_config_file>"
    exit 1
fi

CONFIG_FILE=$1

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file '$CONFIG_FILE' not found"
    exit 1
fi

# Make benchmark script executable
chmod +x benchmark_single.sh

# Get config file name without path and extension
CONFIG_NAME=$(basename "$CONFIG_FILE" .config)

# Initialize markdown file
cat > "${CONFIG_NAME}_results.md" << EOF
# Stencil Computation Benchmark Results for ${CONFIG_NAME}

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |
|-----------|-----------|--------|------------------|------------------|
EOF

echo "Running experiments..."
echo

# Read config file line by line
while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines and comments
    if [[ -z "$line" || "$line" =~ ^# ]]; then
        continue
    fi
    
    # Parse the 5-tuple: width,height,tile_width,tile_height,radius
    IFS=',' read -r width height tile_width tile_height radius <<< "$line"
    
    # Trim whitespace
    width=$(echo "$width" | xargs)
    height=$(echo "$height" | xargs)
    tile_width=$(echo "$tile_width" | xargs)
    tile_height=$(echo "$tile_height" | xargs)
    radius=$(echo "$radius" | xargs)
    
    echo "Testing: Grid ${width}x${height}, Tile ${tile_width}x${tile_height}, Radius ${radius}"
    
    # Run benchmark
    benchmark_result=$(./benchmark_single.sh "$width" "$height" "$tile_width" "$tile_height" "$radius")
    
    # Parse results
    IFS=' ' read -r wse2_cycles wse3_cycles <<< "$benchmark_result"
    
    # Format cycle counts (show -1 as "ERROR")
    if [ "$wse2_cycles" = "-1" ]; then
        wse2_display="ERROR"
    else
        wse2_display="$wse2_cycles"
    fi
    
    if [ "$wse3_cycles" = "-1" ]; then
        wse3_display="ERROR"
    else
        wse3_display="$wse3_cycles"
    fi
    
    # Append result to markdown file immediately
    echo "| ${width}x${height} | ${tile_width}x${tile_height} | $radius | $wse2_display | $wse3_display |" >> "${CONFIG_NAME}_results.md"
    
    echo "  WSE2: $wse2_cycles cycles/iter, WSE3: $wse3_cycles cycles/iter"
    echo
done < "$CONFIG_FILE"

# Add notes at the end
cat >> "${CONFIG_NAME}_results.md" << EOF

**Notes:**
- Cycles/Iter represents average cycles per iteration
- ERROR indicates compilation failure or computation mismatch
- Generated on: $(date)
EOF

echo "Results saved to ${CONFIG_NAME}_results.md"
echo
echo "=== Results Preview ==="
cat "${CONFIG_NAME}_results.md"