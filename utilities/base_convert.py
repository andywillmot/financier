import datetime
import json
import re

class BaseConvert:
    def __init__(self, inputline):
        self.inputline = inputline

        self.output  = {
            "date": "",
            "order": "",
            "ttype": "",
            "account": "",
            "title": "",
            "value": "",
            "validated": "False",
        }

    def validate(self):
        if  (self.isvalid_date() and self.isvalid_order() and self.isvalid_ttype() \
            and self.isvalid_account() and self.isvalid_title() and self.isvalid_value()):
            self.output["validated"] = True
            return True
        else:
            self.output["validated"] = False
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

        if int(self.output["order"]) < 0:
            print("Error-format: Order is not positive")
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


