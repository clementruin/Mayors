import argparse
import sys
import numpy as np
import scrap.init as init
import stats.analyse as analyse
import stats.display as display
import scrap.create_database as create_database

parser = argparse.ArgumentParser()
parser.add_argument('-f','--function', help='Input function',required=True)
parser.add_argument('-a','--argument',help='Output argument', required=False)
args = parser.parse_args()
 
""" 
# Show values
print ("Input function: %s" % args.function )
print ("Input argument: %s" % args.argument )
"""

def main():
    script = sys.argv[0]
    function = sys.argv[2]
    argument = sys.argv[4]
    assert function in ['init_database', 'populate', 'display','analyse'], \
           'Function is not one of init_database, populate, display or analyse: ' + function
    process(function, argument)

def process(function, argument):
    if function == 'init_database':
        init.main()
    elif function == 'populate':
        create_database.main(argument)
    elif function == 'display':
        print("Let me display ...")
    elif function == 'analyse':
        analyse.main(argument)

main()