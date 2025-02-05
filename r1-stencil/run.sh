export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=12,7 --fabric-offsets=4,1 --params=w:4,h:3,steps:100 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out