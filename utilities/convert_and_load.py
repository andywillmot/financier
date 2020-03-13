#!/usr/bin/python

import sys, getopt
import requests
from pathlib import Path
from lbg_convert import LBGConvert, OrderGenerator
import json

SELECTOR = {
    "LBG": LBGConvert
}

BULK_RECORDS_PER_CALL = 50
ENDPOINT = "/transactions/"
AUTH_TOKEN =  "0d09a31b97b45daa0cdc604bbbaad99f66ea8180"

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

    if not host:
        print("Error: Missing host")
        print("-h for help")
        sys.exit(1)

    if not authtoken:
        print("Error: Missing auth token")
        print("-h for help")
        sys.exit(1)

#    print ('Input file is ', inputfile)
#    print ('Format is ', fileformat)
    return fileformat, inputfile, host, authtoken, dryrun


def main(argv):
    fileformat, inputfile, host, authtoken, dryrun = test_parameters(argv)

    #validate format
    if fileformat not in SELECTOR:
        print("Conversion type", fileformat,"not found")
        exit(1)

    bulk_load_data = []
    bulk_counter = 0

    requesturl = "http://" + host + ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token " + authtoken
    } 

    # open file
    plfile = Path(inputfile)

    order = 0
    current_date = None
    if plfile.exists():
        with plfile.open(mode='r') as f:
            l = f.readline()
            while(l != ""):
                line_convertor = SELECTOR[fileformat.upper()](l)
                l = f.readline() #read next line early to know to process bulks

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
                        if BULK_RECORDS_PER_CALL > 1:
                            bulk_load_data.append(line_convertor.to_json())
                            if len(bulk_load_data) >= BULK_RECORDS_PER_CALL or l == "":
                                print("Sending bulk load of", BULK_RECORDS_PER_CALL, "records...")
                                print(json.dumps(bulk_load_data))
                                if (not dryrun):
                                    response = requests.post(url = requesturl, headers = headers, \
                                                            data = json.dumps(bulk_load_data))
                                    if response.status_code != 201:
                                        print(response.status_code, response.text)
                                bulk_load_data.clear()
                        else:
                            data = line_convertor.to_json()
                            print("Sending:", json.dumps(data))
                            if (not dryrun):
                                response = requests.post(url = requesturl, headers = headers, \
                                                        data = json.dumps(data))
                                if response.status_code != 201:
                                    print(response.status_code, response.text)
                            
                    else:
                        print("Validation Error in:", line_convertor.to_json())
                else:
                    print("Decompose error in: ",str(l))
    else:
        print("Error: File", inputfile, "does not exist.")


if __name__ == "__main__":
   main(sys.argv[1:])

    
