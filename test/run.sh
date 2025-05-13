export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=9,3 --fabric-offsets=4,1 --params=M:400 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out