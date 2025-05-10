export SINGULARITYENV_SIMFABRIC_DEBUG=landing
cslc layout.csl --fabric-dims=16,12 --fabric-offsets=4,1 --params=w:16,h:16,tile_width:3,tile_height:3,radius:2,num_iterations:20 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out