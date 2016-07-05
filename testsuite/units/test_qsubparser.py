#!/bin/env python
# Test Qsubfile Class


import os.path 
import sys
import tempfile
import subprocess

import unittest

from torquefilter.parser.qsub import qsub

class test_qsub_parser(unittest.TestCase):

    def setUp (self):
        self.current = qsub()

    def test_parse_options(self):
        "Check that parse_qsub parses options"

        args = "-l nodes=1:ppn=3,pvmem=5GB -q standby".split ()
        attributes = vars(self.current.parse_args(args))

        self.assertEqual(attributes['resource_list'], 
                ['nodes=1:ppn=3,pvmem=5GB'])
        self.assertEqual(attributes['destination'], ['standby'])


if __name__ == '__main__':
    unittest.main()
