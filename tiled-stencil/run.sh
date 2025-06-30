export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace

WIDTH=100
HEIGHT=100
TILE_WIDTH=20
TILE_HEIGHT=20
RADIUS=1
NUM_ITERATIONS=2
ARCH="wse3"

# increase width and height so they are multiples of tile_width and tile_height
INNER_W=$((WIDTH - 2 * RADIUS))
INNER_H=$((HEIGHT - 2 * RADIUS))

REMAINDER_W=$((INNER_W % TILE_WIDTH))
REMAINDER_H=$((INNER_H % TILE_HEIGHT))

if [ $REMAINDER_W -ne 0 ]; then
  PAD_W=$((TILE_WIDTH - REMAINDER_W))
  echo "increasing width from $WIDTH to $((WIDTH + PAD_W))"
  WIDTH=$((WIDTH + PAD_W))
fi

if [ $REMAINDER_H -ne 0 ]; then
  PAD_H=$((TILE_HEIGHT - REMAINDER_H))
  echo "increasing height from $HEIGHT to $((HEIGHT + PAD_H))"
  HEIGHT=$((HEIGHT + PAD_H))
fi

NUM_PE_X=$(((WIDTH - 2 * RADIUS) / TILE_WIDTH + 2))
NUM_PE_Y=$(((HEIGHT - 2 * RADIUS) / TILE_HEIGHT + 2))


cslc layout.csl \
--fabric-dims=$((NUM_PE_X+7)),$((NUM_PE_Y+2)) \
--fabric-offsets=4,1 \
--params=w:$WIDTH,h:$HEIGHT,tile_width:$TILE_WIDTH,tile_height:$TILE_HEIGHT,radius:$RADIUS \
--memcpy \
--channels=1 \
--arch=$ARCH \
--max-inlined-iterations=1000000 \
-o out
# --link-section-start-address-bytes=".own_values:20960,.buffer:40960" \
if [ $? -ne 0 ]; then
  echo "cslc failed" >&2
  exit 1
fi
cs_python run.py --name out --num-iterations $NUM_ITERATIONS >> python.log
if [ $? -ne 0 ]; then
    echo "cerebras computation doesn't match python computation" >&2
    exit 1
else
    echo "Success!"
fi
python3 filter_traces.py <<EOF
5
2
EOF
echo "Total Cerebras cycles:"
python3 get_cycles.py