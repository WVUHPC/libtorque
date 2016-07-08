#!/bin/env python
# Test Qsubfile Class


import unittest

from torquefilter.PBSjob.parser.qsub import qsub

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

    def test_remainder(self):
        "Check that parse_qsub handles leftover options"

        args="-l nodes=1:ppn=3,pvmem=5GB -q standy something_else that".split()
        attributes = vars(self.current.parse_args(args))

        self.assertEqual(attributes['remain'], ['something_else', 'that'])
        
        leftovers = attributes['remain']
        self.assertEqual(len(leftovers), 2)


if __name__ == '__main__':
    unittest.main()
