export SINGULARITYENV_SIMFABRIC_DEBUG=inst_trace
cslc layout.csl --fabric-dims=16,12 --fabric-offsets=4,1 --params=w:14,h:14,tile_width:6,tile_height:6,radius:1,num_iterations:10 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out