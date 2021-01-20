#!/usr/bin/python

import sys, getopt
import requests
from pathlib import Path
from base_convert import OrderGenerator
from lbg_convert import LBGFileConvert, LBGRecordConvert
import json

SELECTOR = {
    "LBG": LBGFileConvert,
}


ENDPOINT = "/transactions/"
AUTH_TOKEN =  "0d09a31b97b45daa0cdc604bbbaad99f66ea8180"

def print_help_and_exit():
    print ('import_file.py -f <format> -i <inputfile> -t <token> -o <host> [-d]')
    print ('List of available formats:')
    print ('Lloyds Bank Export     -f LBG')
    print ('AMEX Export            -f AMEX')
    print ('HSBC Export            -f HSBC')
    sys.exit(2)

# validate parameters
def test_parameters(argv):
    inputfile = ''
    fileformat = ''
    host = ''
    authtoken = ''
    dryrun = False

    try:
        opts, args = getopt.getopt(argv,"f:i:t:o:d",["format=","inputfile=","token=","host=","dryrun"])
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
        elif opt in ("-o", "--host"):
            host = arg
        elif opt in ("-t", "--token"):
            authtoken = arg
        elif opt in ("-d", "--dryrun"):
            dryrun = True

    if not inputfile:
        print("Error: Missing input file")
        print("-h for help")
        sys.exit(1)

    if not fileformat:
        print("Error: Missing format")
        print("-h for help")
        sys.exit(1)

    if fileformat not in SELECTOR:
        print("Conversion type", fileformat,"not found")
        print("-h for help")
        sys.exit(1)

    if not host:
        print("Error: Missing host")
        print("-h for help")
        sys.exit(1)

    if not authtoken:
        print("Error: Missing auth token")
        print("-h for help")
        sys.exit(1)

    return fileformat, inputfile, host, authtoken, dryrun


def main(argv):
    
    #verify parameters
    fileformat, inputfile, host, authtoken, dryrun = test_parameters(argv)

    #setup http request and headers
    requesturl = "http://" + host + ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token " + authtoken
    } 

    # setup converter object instances
    fileconverter = SELECTOR[fileformat.upper()](Path(inputfile))
    
#    order = 0
#    current_date = None

    if fileconverter.file_exists():
        # get pre-converted file - allows stuff to be done to file before loading
        if fileconverter.pre_convert_file():

            if fileconverter.load_file_records(requesturl, headers, dryrun):
                print("Success. Your records should have been loaded")
            else:
                print("Error: Loading records")
        else:
            print("Error: Pre-converting file")
    else:
        print("Error: File", inputfile, "does not exist.")


if __name__ == "__main__":
   main(sys.argv[1:])

    
