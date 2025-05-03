export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=14,9 --fabric-offsets=4,1 --params=w:6,h:6,tile_width:2,tile_height:2,rank:1,num_iterations:1 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out