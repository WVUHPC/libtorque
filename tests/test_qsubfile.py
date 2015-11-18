#!/bin/env python
# Test Qsubfile Class


import os.path, sys
import tempfile
import unittest

sys.path.append (os.path.realpath ("../libtorque"))
from qsubfile import qsubfile

class TestQsubfileMethods (unittest.TestCase):
    "Test Qsubfile class methods"

    def setUp (self):
        self.current = qsubfile ()

    def test_strip_command (self):
        command = "<file1 qsub -N file >>output.txt"
        self.assertEqual (self.current.parse_comm (command), ['qsub -N file']) 

    def test_parseOpts (self):
        args = "-l nodes=1:ppn=3,pvmem=5GB -q standby -l ppn=5".split ()
        self.current.parseOpts (args)
        self.assertEqual (self.current.attr ['ppn'], "5")
        self.assertEqual (self.current.attr ['queue'], "standby")

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

    def test_processfile (self):
        qsubfile = "#!/bin/sh\n#PBS -l nodes=1:ppn=3,pvmem=5GB\n" +  \
            "#PBS -q standby\nmodule load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"
        tmpfile = tempfile.NamedTemporaryFile (mode='w', delete=False)
        tmpfile.write (qsubfile)
        filename = tmpfile.name
        tmpfile.close ()
        self.current.processfile (filename)
        self.assertEqual (self.current.attr ['queue'], "standby")
        self.assertEqual (self.current.attr ['nodes'], "1")
        self.assertTrue ("module" in self.current.comm[0:][0])
        os.unlink (filename)
        

if __name__ == '__main__':
    unittest.main()
