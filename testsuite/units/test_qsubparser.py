#!/bin/env python
# Test Qsubfile Class


import os.path 
import sys
import tempfile
import subprocess

import unittest

from torquefilter.qsub.qsubfile import parse_qsub

class test_qsub_parser(unittest.TestCase):

    def setUp (self):
        self.current = parse_qsub()

    def test_parse_options(self):
        "Check that parse_qsub parses options"

        args = "-l nodes=1:ppn=3,pvmem=5GB -q standby -l ppn=5".split ()
        attributes = vars(self.current.parse_args(args))

        self.assertEqual(attributes['ppn'], 5)
        self.assertEqual(attributes['queue'], "standby")
    test_parse_options.parse_qsub = True
    test_parse_options.unit = True


if __name__ == '__main__':
    unittest.main()
