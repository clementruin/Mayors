"""
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
"""


import argparse
__author__ = 'nixCraft'
 
parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
parser.add_argument('-f','--function', help='Input function',required=True)
parser.add_argument('-a','--argument',help='Output argument', required=False)
args = parser.parse_args()
 
## show values ##
print ("Input file: %s" % args.function )
print ("Output file: %s" % args.argument )