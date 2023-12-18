import argparse
import time

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add command-line arguments
parser.add_argument('--flag', action='store_true', help='A boolean flag')
parser.add_argument('--number', type=int, help='A numerical value')
parser.add_argument('--array', nargs='+', help='An array of values')

# Parse the command-line arguments
args = parser.parse_args()

# Print the received parameters
print(f'Flag: {args.flag}')
print(f'Number: {args.number}')
print(f'Array: {args.array}')
time.sleep(30)
