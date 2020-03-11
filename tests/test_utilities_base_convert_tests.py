from utilities.base_convert import BaseConvert
import unittest


class Test_TestDateValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_blank(self):
        self.assertFalse(self.obj.isvalid_date())

    def test_notdate(self):
        self.obj.output["date"] = "NOT A DATE"
        self.assertFalse(self.obj.isvalid_date())
    
    def test_validdate(self):
        self.obj.output["date"] = "2009-03-12"
        self.assertTrue(self.obj.isvalid_date())
    
class Test_TestOrderValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_blank(self):
        self.assertFalse(self.obj.isvalid_order())
    
    def test_notinteger(self):
        self.obj.output["order"] = "kjh"
        self.assertFalse(self.obj.isvalid_order())
    
    def test_greaterorqualtozero(self):
        self.obj.output["order"] = "-3"
        self.assertTrue(self.obj.isvalid_order())
    
    def test_isvalid(self):
        self.obj.output["order"] = "5"
        self.assertTrue(self.obj.isvalid_order())

class Test_TestAccountValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_isblankfail(self):
        self.assertFalse(self.obj.isvalid_account())
      
    def test_31longstringfail(self):
        self.obj.output["account"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertFalse(self.obj.isvalid_account())
    
    def test_30longstringvalid(self):
        self.obj.output["account"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertTrue(self.obj.isvalid_account())

    def test_isvalid(self):
        self.obj.output["account"] = "Lloyds 123456789"
        self.assertTrue(self.obj.isvalid_account())

class Test_TestValueValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_blank(self):
        self.assertFalse(self.obj.isvalid_value())
    
    def test_isnumber(self):
        self.obj.output["value"] = "sometext"
        self.assertFalse(self.obj.isvalid_value())
    
    def test_numbertoohigh(self):
        self.obj.output["value"] = "111111111"
        self.assertFalse(self.obj.isvalid_value())

    def test_numbertoolow(self):
        self.obj.output["value"] = "-111111111"
        self.assertFalse(self.obj.isvalid_value())

    def test_invaliddecimal(self):
        self.obj.output["value"] = "12.232"
        self.assertFalse(self.obj.isvalid_value())        

    def test_invaliddecimal(self):
        self.obj.output["value"] = ".232"
        self.assertFalse(self.obj.isvalid_value()) 

    def test_isvaliddecimal(self):
        self.obj.output["value"] = "12.1"
        self.assertTrue(self.obj.isvalid_value())
    
    def test_isvaliddecimal(self):
        self.obj.output["value"] = "-12.1"
        self.assertTrue(self.obj.isvalid_value()) 

    def test_isvalidint(self):
        self.obj.output["value"] = "12"
        self.assertTrue(self.obj.isvalid_value()) 

    def test_isvalid(self):
        self.obj.output["value"] = "40.56"
        self.assertTrue(self.obj.isvalid_value())


class Test_TestTTypeValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_blankok(self):
        self.assertTrue(self.obj.isvalid_ttype())
    
    def test_11longstringfail(self):
        self.obj.output["ttype"] =  "AAAAAAAAAAA"
        self.assertFalse(self.obj.isvalid_ttype())
    
    def test_10longstringvalid(self):
        self.obj.output["ttype"] =  "AAAAAAAAAA"
        self.assertTrue(self.obj.isvalid_ttype())

    def test_isvalid(self):
        self.obj.output["ttype"] = "DEB"
        self.assertTrue(self.obj.isvalid_ttype())

class Test_TestTitleValidation(unittest.TestCase):
    def setUp(self):
        self.obj = BaseConvert("")

    def test_blank(self):
        self.assertFalse(self.obj.isvalid_title())

    def test_246longstringfail(self):
        self.obj.output["title"] =  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertFalse(self.obj.isvalid_title())
    
    def test_245longstringvalid(self):
        self.obj.output["title"] =  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + \
                                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertTrue(self.obj.isvalid_title())
    
    def test_isvalid(self):
        self.obj.output["title"] = "This is a transaction title"
        self.assertTrue(self.obj.isvalid_title())



if __name__ == '__main__':
    unittest.main()
