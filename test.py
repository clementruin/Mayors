"""
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
"""


import argparse
 
parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
parser.add_argument('-f','--function', help='Input function',required=True)
parser.add_argument('-a','--argument',help='Output argument', required=False)
args = parser.parse_args()
 
## show values ##
print ("Input file: %s" % args.function )
print ("Output file: %s" % args.argument )


#####

import sys
import numpy as np

def main():
    script = sys.argv[0]
    action = sys.argv[1]
    filenames = sys.argv[2:]
    assert action in ['--min', '--mean', '--max'], \
           'Action is not one of --min, --mean, or --max: ' + action
    for f in filenames:
        process(f, action)

def process(filename, action):
    data = np.loadtxt(filename, delimiter=',')

    if action == '--min':
        values = data.min(axis=1)
    elif action == '--mean':
        values = data.mean(axis=1)
    elif action == '--max':
        values = data.max(axis=1)

    for m in values:
        print(m)

main()