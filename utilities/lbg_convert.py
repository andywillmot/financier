from base_convert import BaseConvert, OrderGenerator
from datetime import datetime

class LBGConvert(BaseConvert):
    order_handling = OrderGenerator.ReverseFileOrderGeneration

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
            value = "-0" + fields[5] if fields[5][0] == "." else "-" + fields[5]
        else:    
            value = "0" + fields[6] if fields[6][0] == "." else fields[6]

        self.output["value"] = value
        
        if not self.isvalid_value():
            return False
        
        return True


        
