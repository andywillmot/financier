from base_convert import *
from datetime import datetime
from pathlib import Path
import csv



class LBGRecordConvert(BaseRecordConvert):
    order_handling = OrderGenerator.ReverseFileOrderGeneration

    def decompose(self):
        fields = self.inputline.split(",")

        #check size
        if len(fields) != 10:
            print("Incorrect number of fields, should be 10")
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
        
        #convert order
        self.output["order"] = str(int(fields[8]))
        if not self.isvalid_order():
            return False

        #convert count
        self.output["count"] = str(int(fields[9]))
        if not self.isvalid_count():
            return False

        return True


class LBGFileConvert(BaseFileConvert):
    records_per_call = 100
    has_header = True
    record_convert_class = LBGRecordConvert

    def pre_convert_file(self):

        outputfilepath = self.inputfilepath.with_name(
                        self.inputfilepath.name + ".tmp"
        )
        
        outputfilepath.touch()
        
        with self.inputfilepath.open(mode='r') as infile, \
             outputfilepath.open(mode='w', newline = '') as outfile:

            index = {}
            order = 0
            current_date = ""
            csvin = csv.DictReader(infile)
            fieldnames = csvin.fieldnames
            fieldnames.append("Order")
            fieldnames.append("Count")
            csvout = csv.DictWriter(outfile, fieldnames=fieldnames)
            csvout.writeheader()
            for row in csvin:
                if (current_date != row['Transaction Date']):
                    index = {}
                    current_date = row['Transaction Date']
                    order = 0
                else:
                    order = order - 1

                key = row['Transaction Type'] + \
                    row['Account Number'] + row['Transaction Description'] + \
                    row['Debit Amount'] + row['Credit Amount']
                if key in index:
                    index[key] = index[key] + 1
                else:
                    index[key] = 0
                count = index[key]
                row['Count']=index[key]
                row['Order']=order
                csvout.writerow(row)

        self.inputfilepath = outputfilepath
        return True
        




        
