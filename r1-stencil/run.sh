export SINGULARITYENV_SIMFABRIC_DEBUG=landing
cslc layout.csl --fabric-dims=50,40 --fabric-offsets=4,1 --params=w:40,h:30,steps:100 --memcpy --channels=1 --arch=wse2 -o out
cs_python run.py --name out