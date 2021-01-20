import datetime
import json
import re
import enum
from pathlib import Path
import requests

class OrderGenerator(enum.Enum):
    NoGeneration = 0
    FileOrderGeneration = 1
    ReverseFileOrderGeneration = 2

class BaseRecordConvert:

    order_handling = OrderGenerator.NoGeneration

    def __init__(self, inputline):
        self.inputline = inputline

        self.output  = {
            "date": "",
            "order": "",
            "count": "",
            "ttype": "",
            "account": "",
            "title": "",
            "value": "",
        }

    def validate(self):
        if  (self.isvalid_date() and self.isvalid_order() and self.isvalid_ttype() \
            and self.isvalid_account() and self.isvalid_title() and self.isvalid_value()):
            return True
        else:
            return False
        
    def isvalid_date(self):
        if self.output["date"] == "": 
            print("Error-format: Date is blank")
            return False
        try:
            test = datetime.datetime.strptime(self.output["date"], '%Y-%m-%d')
        except:
            print("Error-format: Date format incorrect (YYYY-MM-DD)")
            return False
        return True

    def isvalid_order(self):
        if self.output["order"] == "": 
            print("Error-format: Order is blank")
            return False
        try:
            val = int(self.output["order"])
        except:
            print("Error-format: Cannot convert Order to integer")
            return False

        return True

    def isvalid_count(self):
        if self.output["order"] == "": 
            print("Error-format: Count is blank")
            return False

        try:
            val = int(self.output["order"])
        except:
            print("Error-format: Cannot convert Order to integer")
            return False

        return True

    def isvalid_account(self):
        if self.output["account"] == "": 
            print("Error-format: Account is blank")
            return False
        
        if len(self.output["account"]) > 30:
            print("Error-format: account is greater than 30 characters in length")
            return False
        return True

    def isvalid_title(self):
        if self.output["title"] == "": 
            print("Error-format: title is blank")
            return False
        
        if len(self.output["title"]) > 245:
            print("Error-format: title is greater than 245 characters in length")
            return False
        return True

    def isvalid_value(self):
        if self.output["value"] == "": 
            print("Error-format: value is blank")
            return False

        try:
            val = float(self.output["value"])
        except:
            print("Error-format: Cannot convert value to float")
            return False

        #2-digit decimal pattern
        check_pattern = re.compile(r"^-?\d{1,7}(\.\d{1,2})?$")
        if not check_pattern.search(self.output["value"]):
            print("Error-format: value is not 0000000.00 format")
            return False
    
        if float(self.output["value"]) > 99999999 or \
           float(self.output["value"]) < -99999999:
            print("Error-format: value is greater than 10 digits")
            return False
        return True
    
    def isvalid_ttype(self):
        if len(self.output["ttype"]) > 10:
            print("Error-format: ttype is greater than 245 characters in length")
            return False
        return True

    def to_json(self):
        return self.output
    
    def decompose(self):
        pass

    def pre_convert(self, inputfile):
        return inputfile



class BaseFileConvert:
    records_per_call = 1
    has_header = False
    record_convert_class = BaseRecordConvert

    def __init__(self, inputfilepath: Path):
        self.inputfilepath = inputfilepath
        self.formatter_class = self.__class__.record_convert_class
    
    def file_exists(self):
        return self.inputfilepath.exists()
    
    def pre_convert_file(self):
        return True

    def load_file_records(self, requesturl, headers, dryrun=False):

        bulk_load_data = []
        bulk_counter = 0
        recs_per_call = self.__class__.records_per_call
        has_header = self.__class__.has_header
        line_errors = 0

        with self.inputfilepath.open(mode='r') as file:
            line = file.readline()
            if has_header: 
                line = file.readline()
            while (line != ""):
                
                line_convertor = self.formatter_class(line)
                nextline = file.readline() #read next line early to know to process bulks

                if line_convertor.decompose():
                    if line_convertor.validate():
                        if recs_per_call > 1:
                            bulk_load_data.append(line_convertor.to_json())
                            if len(bulk_load_data) >= recs_per_call or nextline == "":
                                print("Sending bulk load of (max)", recs_per_call, "records...")
                                print(json.dumps(bulk_load_data))
                                if (not dryrun):
                                    response = requests.post(url = requesturl, headers = headers, \
                                                            data = json.dumps(bulk_load_data))
                                    if response.status_code != 201:
                                        print(response.status_code, response.text)
                                        return False
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
                        line_errors = line_errors + 1

                else:
                    print("Decompose error in: ",str(line))
                    line_errors = line_errors + 1

                line = nextline
        
        if line_errors > 0:
            print("There ", "was" if line_errors == 1 else "where", line_errors, \
                "validation", "error" if line_errors== 1 else "errors", "in total")
            return False
        else:
            return True    
