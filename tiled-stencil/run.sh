export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=14,9 --fabric-offsets=4,1 --params=w:12,h:12,tile_width:3,tile_height:2,rank:2,num_iterations:20 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out