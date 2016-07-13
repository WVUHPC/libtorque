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

        self.assertEqual(attributes['destination'], ['standby'])

    def test_remainder(self):
        "Check that parse_qsub handles leftover options"

        args="-l nodes=1:ppn=3,pvmem=5GB -q standy something_else that".split()
        attributes = vars(self.current.parse_args(args))

        self.assertEqual(attributes['remain'], ['something_else', 'that'])
        
        leftovers = attributes['remain']
        self.assertEqual(len(leftovers), 2)

    def test_defaultRemainder(self):
        "Check that parse_qsub always produces a remainder"

        args="-l nodes=1:ppn=3,pvmem=5GB".split()
        attributes = vars(self.current.parse_args(args))

        number = len(attributes['remain'])
        self.assertEqual(number, 0)

    def test_resouce_action(self):
        "Check that parse_qsub appends multiple resource options"

        args="-l nodes=1:ppn=3 -l pvmem=5gb -q standby".split()
        attributes = vars(self.current.parse_args(args))

        self.assertEqual(attributes['resource_list'], [['nodes=1:ppn=3'], 
            ['pvmem=5gb']])

    def test_h_option(self):
        "Test that parse_qsub parse '-h' option correctly"

        args="-h".split()
        attributes = vars(self.current.parse_args(args))

        self.assertTrue(attributes['user_hold']) 


if __name__ == '__main__':
    unittest.main()
