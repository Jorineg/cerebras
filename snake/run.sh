cslc layout.csl \
 --fabric-dims=14,3 \
 --fabric-offsets=4,1 \
 --params=length:7 \
 --memcpy \
 --channels=1 \
 --arch=wse2 \
 -o out

cs_python run.py --name out &
PYTHON_PID=$!
echo "Python process started with PID $PYTHON_PID"
echo "To stop it, run: kill $PYTHON_PID"

wait $PYTHON_PID