export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=14,8 --fabric-offsets=4,1 --params=w:6,h:5,steps:1 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out