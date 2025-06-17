export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace

WIDTH=4
HEIGHT=4
NUM_ITERATIONS=8
ARCH="wse3"

cslc layout.csl \
--fabric-dims=$((WIDTH+7)),$((HEIGHT+2)) \
--fabric-offsets=4,1 \
--params=w:$WIDTH,h:$HEIGHT,steps:$NUM_ITERATIONS \
--memcpy \
--channels=1 \
--arch=$ARCH \
--max-inlined-iterations=1000000 \
-o out
if [ $? -ne 0 ]; then
  echo "cslc failed" >&2
  exit 1
fi
cs_python run.py --name out >> python.log
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


# original
# export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
# cslc layout.csl --fabric-dims=14,9 --fabric-offsets=4,1 --params=w:4,h:3,steps:10 --memcpy --channels=1 --arch=wse2 -o out
# cs_python run.py --name out