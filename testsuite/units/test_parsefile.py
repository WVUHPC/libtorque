#!/bin/env python

import os.path
import sys
import tempfile
import subprocess

import unittest

from torquefilter.qsub.parser import parsefile


class dummy_map:
    status  = None
    attribute = {}
    commands = []

class dummy_parser(dummy_map):

    def add_command(self, command):
        self.commands.append[command]

    def add_directive(self, directive):
        self.attribute[directive[0]] = directive[1]

class test_process_file(unittest.TestCase):

    def setUp (self):
        self.map = dummy_parser()
        self.current = parsefile(self.map)

    def test_strip_command(self):
        "Check complex command structures"
        command = "<file1 qsub -N file >>output.txt"
        self.current.parse_command(command)
        self.assertEqual(self.map.commands, ['qsub -N file'])

        command = "<file1 cat | cmp - file2"
        self.current.parse_command(command)
        self.assertEqual(self.map.commands, ['cat', 'cmp - file2'])
    test_strip_command.unit = True
    test_strip_command.parsefile = True

    def test_identify_commands(self):
        "Check runparser identifies commands"
        qsubfile = "qsub -N stuff\n"

        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.runparser(filename, printfile=False)
        self.assertEqual(self.map.commands,['qsub -N stuff'])
    test_identify_commands.unit = True
    test_identify_commands.parsefile = True

    def test_identify_directive(self):
        "Check runparser identifies directives"
        qsubfile = "#PBS -N stuff\n"

        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.runparser(filename, printfile=False)
        self.assertEqual(self.map.attribute['name'],['stuff'])
    test_identify_directive.unit = True
    test_identify_directive.parsefile = True

    def test_processfile(self):
        "Check runparsser takes files as input"
        qsubfile = "#!/bin/sh\n#PBS -l nodes=1:ppn=3,pvmem=5GB\n" +  \
            "#PBS -q standby\nmodule load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        self.current.processfile(filename, printfile=False)
        self.assertEqual(self.map.attribute['queue'], "standby")
        self.assertEqual(self.map.attribute['nodes'], "1")
        self.assertTrue("module" in self.map.commands[0:][0])
        os.unlink(filename)
    test_processfile.unit = True
    test_processfile.parsefile = True
        
    def test_identical_output(self):
        "Check runparser produces identical output"

        qsubfile = "#!/bin/sh\n#PBS -l nodes=1:ppn=3,pvmem=5GB\n" +  \
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

        # Submit file into processfile () - writing STDOUT to tmpoutfile
        self.current.processfile(filename, outfile=tmpoutfile)
        shellcmd = ['cmp', filename, tmpoutfile]
        self.assertEqual(subprocess.call(shellcmd), 0)
      
        os.unlink(filename)
        os.unlink(tmpoutfile)
    test_identical_output.unit = True
    test_identical_output.parsefile = True

if __name__ == '__main__':
    unittest.main()
