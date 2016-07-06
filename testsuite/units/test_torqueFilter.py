
#!/bin/env python
# Test torquefilter class


import os.path, sys
import unittest

import torquefilter as tf

class TestTorqueFilterMethods(unittest.TestCase):
    "Test submitfilter main methods with all standard "

    def setUp(self):
        class testFilter(tf.torqueFilter):
            
            def __init__(self, mapper=tf.PBSmap, parser=tf.qsub 
                    scanner=tf.scanner):
                self.filename   =   None
                self.map        =   mapper()
                self.parser     =   parser()
                self.scanner    =   scanner(self.map, self.parser)
                

        self.current = testFilter() 

    def test_rtn_filename(self):
        sys.argv = []
        self.current.rtn_filename()
        self.assertEqual(self.current.filename, "STDIN")
        sys.argv = ("filename -l nodes=1 pbsfile.sh".split())
        self.current.rtn_filename()
        self.assertEqual(self.current.filename, "pbsfile.sh")




if __name__ == '__main__':
    unittest.main()

