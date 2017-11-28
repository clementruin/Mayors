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
parser.add_argument('-l', '--list', help = 'Gives the list of all the available functions', action = "store_true")
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
        sub_function = sys.argv[3]
        argument = sys.argv[4]
        argtype = type(argument)
    elif len(sys.argv) == 3:
        argument = sys.argv[3]
        argtype = type(argument)
    else :
        sub_function = "None"
        argument = "None"
        argtype = "None"
    assert function in ['init_database', 'populate', 'display','analyse'], \
           'Function is not one of init_database, populate, display or analyse: ' + function
    assert sub_function in ['pop_per_party', 'party_vs_citysize1', 'party_vs_citysize2'], \
           'Sub function is not one of pop_per_party, party_vs_citysize1 or party_vs_citysize2 : ' + sub_function       
    process(function, sub_function, argument, argtype)

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


def process(function, sub_function, argument, argtype):
    if function == 'init_database':
        init.main()
    elif function == 'populate':
        create_database.main(argument, argtype)
    elif function == 'display':
        print("Let me display ...")
    elif function == 'analyse':
        df = analyse.builder()
        if sub_function == 'pop_per_party':
            analyse.pop_per_party(range)
        elif sub_function == 'party_vs_citysize1':
            analyse.party_vs_citysize1(df)
        elif sub_function == 'party_vs_citysize2':
            analyse.party_vs_citysize2(df)
        elif args.list :
            print('list of available functions',
                  '\n','pop_per_party', 'RANGE', '     |     ', 'give the population per party',
                  '\n','party_vs_citysize1', 'DATAFRAME', '     |     ', 'display the percentage of mayor per party given the size of the city',
                  '\n','party_vs_citysize2', 'DATAFRAME', '     |     ', 'display the size of the population per party (%) given the size of the city')

main()