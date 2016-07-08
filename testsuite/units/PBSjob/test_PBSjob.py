#!/bin/env python
# Test Qsubfile Class


import unittest

from torquefilter.PBSjob.pbsjob import PBSjob

class test_qsub_parser(unittest.TestCase):

    def test_class_instance(self):
        "Check that PBSjob can be initialized"

        args = "qsub -l nodes=1:ppn=3,pvmem=5GB -q standby".split ()

        current = PBSjob(args)

        self.assertEqual(current.filename, 'STDIN')
        self.assertEqual(current.attributes['destination'], ['standby'])


if __name__ == '__main__':
    unittest.main()
