import re

def main():
    # Get user input for x and y coordinates
    x = input("Enter the x coordinate: ")
    y = input("Enter the y coordinate: ")

    # Define the pattern to match the lines with the given coordinates and not containing 'IDLE'
    pattern = re.compile(rf'@.* P{x}\.{y}: .*')

    # Read the sim.log file and filter the lines
    with open('sim.log', 'r') as infile, open('sim_filtered.log', 'w') as outfile:
        for line in infile:
            if pattern.search(line):
                # check that line does not contain 'IDLE' or 'NOP'
                # if 'IDLE' not in line and 'NOP' not in line:
                outfile.write(line)

if __name__ == "__main__":
    main()