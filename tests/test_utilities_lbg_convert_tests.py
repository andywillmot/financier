from utilities.lbg_convert import *
import filecmp
import os
import unittest


class Test_TestPreConvert(unittest.TestCase):
    def setUp(self):
        thefile = os.getcwd() + "\\tests\\nodups.txt"
        self.obj = LBGFileConvert(Path(thefile), LBGRecordConvert)

    def test_existstest(self):
        self.assertTrue(self.obj.file_exists())
        
    def test_filenotsame(self):
        infile = self.obj.inputfilepath
        self.obj.pre_convert_file()
        outfile = self.obj.inputfilepath
        self.assertFalse(filecmp.cmp(infile,outfile))


if __name__ == '__main__':
    unittest.main()