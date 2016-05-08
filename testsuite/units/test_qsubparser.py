#!/bin/env python
# Test Qsubfile Class


import os.path 
import sys
import tempfile
import subprocess

import unittest

from torquefilter.qsub.qsubfile import qsubfile

class test_qsub_parser(unittest.TestCase):

    def setUp (self):
        self.current = qsubfile()

    def test_strip_command(self):
        command = "<file1 qsub -N file >>output.txt"
        self.assertEqual (self.current.parse_comm (command), ['qsub -N file']) 

    def test_parseOpts(self):
        args = "-l nodes=1:ppn=3,pvmem=5GB -q standby -l ppn=5".split ()
        self.current.parseOpts (args)
        self.assertEqual (self.current.attr ['ppn'], "5")
        self.assertEqual (self.current.attr ['queue'], "standby")

    def test_walltime_parseOpts(self):
        args = "-l nodes=4:ppn=4,pvmem=17gb,walltime=04:00:00".split ()
        self.current.parseOpts ( args )
        self.assertEqual ( self.current.attr ['walltime'], "04:00:00" )

    def test_commline (self):
        args = "-l nodes=1:ppn=3,pvmem=5GB -q standby -l ppn=5".split ()
        self.current.commline (args)
        self.assertEqual (self.current.attr ['ppn'], "5")
        self.assertEqual (self.current.attr ['queue'], "standby")

    def test_CLI_over_parseOpts (self):
        cli_args = "-l nodes=1:ppn=3,pvmem=5GB -q standby".split ()
        args = "-l nodes=2:ppn=5 -q comm_mmem_week".split ()
        self.current.parseOpts (args)
        self.current.commline (cli_args)
        self.assertEqual (self.current.attr ['ppn'], "3")
        self.assertEqual (self.current.attr ['queue'], "standby")

    def test_parseOpts_return (self):
        args = "-l nodes=1:ppn=3 filename".split ()
        leftover = self.current.parseOpts (args)
        self.assertEqual (len (leftover), 1)
        self.assertEqual (leftover [0], 'filename')

if __name__ == '__main__':
    unittest.main()
