import argparse
import sys
import numpy as np
import scrap.init as init 
import scrap.create_database as create_database
import stats.display as display
import stats.analyse as analyse

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
    """Retrieves and assert user's input
    """
    script = sys.argv[0]
    function = sys.argv[2]
    if len(sys.argv)>=4 :
        argument = sys.argv[4]
        argtype = type(argument)
    else :
        argument = "None"
        argtype = "None"
    assert function in ['init_database', 'populate', 'display','analyse'], \
           'Function is not one of init_database, populate, display or analyse: ' + function
    process(function, argument, argtype)

def type(arg):
    """Determines the type of argument : 
    Did the user type a department number, city, or postal code?
    """
    try :
        if int(arg) >= 1 and int(arg) <= 98:
            return 'dpt'
        elif int(arg) >= 1000 and int(arg) < 99000:
            return 'postal_code'
    except :
        return 'other'


def process(function, argument, argtype):
    if function == 'init_database':
        init.main()
    elif function == 'populate':
        create_database.main(argument, argtype)
    elif function == 'display':
        print("Let me display ...")
    elif function == 'analyse':
        analyse.builder()

main()