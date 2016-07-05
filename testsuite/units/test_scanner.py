#!/bin/env python

import os.path
import sys
import tempfile
import subprocess

import unittest
import argparse

from torquefilter.scanner.scanner import scanner


class dummy_map:
    
    def __init__(self):
        self.attribute = {}
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def add_attribute(self, directive):
        for key in directive.keys():
            self.attribute[key] = directive[key]


class test_scanner(unittest.TestCase):

    def setUp(self):
        self.map = dummy_map()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-N', dest='name', nargs=1)
        self.parser.add_argument('-q', dest='queue', nargs=1)
        self.current = scanner(self.map, self.parser)

    def test_strip_command(self):
        "Check complex command structures"

        command = "<file1 qsub -N file >>output.txt"
        rt_cmd = self.current.parse_command(command)
        self.assertEqual(rt_cmd, ['qsub -N file'])

        command = "<file1 cat | cmp - file2"
        rt_cmd = self.current.parse_command(command)
        self.assertEqual(rt_cmd, ['cat', 'cmp - file2'])

    def test_identify_commands(self):
        "Check runparser identifies commands"

        qsubfile = "qsub -N stuff\n"

        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.runparser(filename, printfile=False)
        self.assertEqual(self.map.commands,['qsub -N stuff'])

    def test_identify_directive(self):
        "Check runparser identifies directives"

        qsubfile = "#PBS -N stuff\n"

        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.runparser(filename, printfile=False)
        self.assertEqual(self.map.attribute['name'],['stuff'])

    def test_processfile(self):
        "Check runparser takes files as input"

        qsubfile = "#!/bin/sh\n#PBS -q standby\n" \
                + "module load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.runparser(filename, printfile=False)
        self.assertEqual(self.map.attribute['queue'], ['standby'])
        self.assertTrue("module" in self.map.commands[0:][0])
        os.unlink(filename)
        
    def test_identical_output(self):
        "Check runparser produces identical output"

        qsubfile = "#!/bin/sh\n" +  \
            "#PBS -q standby\nmodule load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"

        # Create sample submission script ; and capture output
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()
        
        expect_tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpoutfile = expect_tmp.name
        expect_tmp.close()

        # Submit file into runparser() - writing STDOUT to tmpoutfile
        self.current.runparser(filename, outfile=tmpoutfile)
        shellcmd = ['cmp', filename, tmpoutfile]
        self.assertEqual(subprocess.call(shellcmd), 0)
      
        os.unlink(filename)
        os.unlink(tmpoutfile)

if __name__ == '__main__':
    unittest.main()
