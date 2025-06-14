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

# Initialize results
results=()

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
    
    # Store results
    results+=("$width|$height|$tile_width|$tile_height|$radius|$wse2_cycles|$wse3_cycles")
    
    echo "  WSE2: $wse2_cycles cycles/iter, WSE3: $wse3_cycles cycles/iter"
    echo
done < "$CONFIG_FILE"

# Generate markdown table
echo "Generating results table..."
echo

# Create markdown file
cat > experiment_results.md << 'EOF'
# Stencil Computation Benchmark Results

This table shows the average cycles per iteration for different grid sizes, tile sizes, and radius values on WSE2 and WSE3 architectures.

EOF

echo "| Grid Size | Tile Size | Radius | WSE2 Cycles/Iter | WSE3 Cycles/Iter |" >> experiment_results.md
echo "|-----------|-----------|--------|------------------|------------------|" >> experiment_results.md

# Add results to table
for result in "${results[@]}"; do
    IFS='|' read -r width height tile_width tile_height radius wse2_cycles wse3_cycles <<< "$result"
    
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
    
    echo "| ${width}x${height} | ${tile_width}x${tile_height} | $radius | $wse2_display | $wse3_display |" >> experiment_results.md
done

echo "" >> experiment_results.md
echo "**Notes:**" >> experiment_results.md
echo "- Cycles/Iter represents average cycles per iteration" >> experiment_results.md
echo "- ERROR indicates compilation failure or computation mismatch" >> experiment_results.md
echo "- Generated on: $(date)" >> experiment_results.md

echo "Results saved to experiment_results.md"
echo
echo "=== Results Preview ==="
cat experiment_results.md 