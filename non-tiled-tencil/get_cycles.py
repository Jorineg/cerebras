import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "sim_filtered.log"

try:
    with open(filename, "r") as f:
        last_line = f.read().strip().split("\n")[-1]
        cycle = int(last_line.split(" ")[0][1:])
        print(cycle)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)