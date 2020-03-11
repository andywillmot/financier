#!/usr/bin/python

import sys, getopt
from pathlib import Path
from lbg_convert import LBGConvert, OrderGenerator

SELECTOR = {
    "LBG": LBGConvert
}

BULK_RECORDS_PER_CALL = 2

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

    #validate format
    if fileformat not in SELECTOR:
        print("Conversion type", fileformat,"not found")
        exit(1)

    # open file
    plfile = Path(inputfile)

    order = 0
    current_date = None
    if plfile.exists():
        with plfile.open(mode='r') as f:
            l = f.readline()
            while(l != ""):
                line_convertor = SELECTOR[fileformat.upper()](l)

                if line_convertor.decompose():

                    if line_convertor.__class__.order_handling == OrderGenerator.FileOrderGeneration:
                        if current_date != line_convertor.output["date"]:
                            current_date = line_convertor.output["date"]
                            order = 0
                        line_convertor.output["order"] = str(order)
                        order = order + 1

                    if line_convertor.__class__.order_handling == OrderGenerator.ReverseFileOrderGeneration:
                        if current_date != line_convertor.output["date"]:
                            current_date = line_convertor.output["date"]
                            order = 0
                        line_convertor.output["order"] = str(order)
                        order = order - 1

                    if line_convertor.validate():
                        print(line_convertor.to_json())
                    else:
                        print("Validation Error in:", line_convertor.to_json())
                else:
                    print("Decompose error in: ",str(l))

                l = f.readline()
    else:
        print("Error: File", inputfile, "does not exist.")


if __name__ == "__main__":
   main(sys.argv[1:])

    



# load bulk rows
# extract fields from file
# 