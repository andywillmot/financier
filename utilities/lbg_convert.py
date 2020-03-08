from base_convert import BaseConvert
from datetime import datetime

class LBGConvert(BaseConvert):
    order_inc = 1000
    current_date = ""

    def decompose(self):
        fields = self.inputline.split(",")

        #check size
        if len(fields) != 8:
            print("Incorrect number of fields, should be 8")
            return False

        #convert date
        try:
            datetime_object = datetime.strptime(fields[0], "%d/%m/%Y")
            self.output["date"] = datetime_object.strftime('%Y-%m-%d')
        except:
            print("Date cannot be converted")
            return False

        if not self.isvalid_date():
            return False

        #convert ttype
        self.output["ttype"] = fields[1]
        if not self.isvalid_ttype():
            return False
        
        #convert account
        self.output["account"] = "Lloyds: " + fields[3]
        if not self.isvalid_account():
            return False
        
        #convert title
        self.output["title"] = fields[4]
        if not self.isvalid_title():
            return False
        
        #convert value
        if fields[5] != "":
            self.output["value"] = "-" + fields[5]
        else:
            self.output["value"] = fields[6]
        if not self.isvalid_value():
            return False

        #check if i need to decrement the order
        if LBGConvert.current_date != self.output["date"]:
            LBGConvert.current_date = self.output["date"]
            LBGConvert.order_inc = 1000
        else:
            LBGConvert.order_inc = LBGConvert.order_inc - 1

        #insert order
        self.output["order"] = str(LBGConvert.order_inc)

        self.validate()
        
        return True


        
