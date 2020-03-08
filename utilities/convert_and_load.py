#!/usr/bin/python

import sys, getopt
from pathlib import Path


def print_help_and_exit():
    print ('import_file.py -f <format> -i <inputfile>')
    print ('List of available formats:')
    print ('Lloyds Bank Export     -f LBG')
    print ('AMEX Export            -f AMEX')
    print ('HSBC Export            -f HSBC')
    sys.exit(2)

# validate parameters
def test_parameters(argv):
    inputfile = ''
    fileformat = ''

    try:
        opts, args = getopt.getopt(argv,"f:i:",["format=","inputfile="])
    except getopt.GetoptError:
        print_help_and_exit()

    if not opts:
        print_help_and_exit()

    for opt, arg in opts:
        if opt == '-h':
            print_help_and_exit()
        elif opt in ("-f", "--format"):
            fileformat = arg
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
    
    if not inputfile:
        print("Error: Missing input file")
        print("-h for help")
        sys.exit(1)

    if not fileformat:
        print("Error: Missing format")
        print("-h for help")
        sys.exit(1)

#    print ('Input file is ', inputfile)
#    print ('Format is ', fileformat)
    return fileformat, inputfile


def main(argv):
    fileformat, inputfile = test_parameters(argv)
    # get file config
    
        
    # open file
    plfile = Path(inputfile)
    if plfile.exists():
        with plfile.open(mode='r') as f:
            l = f.readline()
            print(l)

    else:
        print("Error: File", inputfile, "does not exist.")


if __name__ == "__main__":
   main(sys.argv[1:])

    



# load bulk rows
# extract fields from file
# 