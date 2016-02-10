#!/bin/env python
# Test Qsubfile Class


import os.path, sys
import tempfile
import subprocess

import unittest

from torquefilter.qsub.qsubfile import qsubfile

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

    def test_walltime_parseOpts ( self ):
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

    def test_processfile ( self ):
        self.current.processfile ( "sample2.pbs", printfile = False )

        self.assertEqual ( self.current.attr ['queue'], "jshawkins" )

    def test_processfile ( self ):
        qsubfile = "#!/bin/sh\n#PBS -l nodes=1:ppn=3,pvmem=5GB\n" +  \
            "#PBS -q standby\nmodule load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile ( mode = 'w', delete = False )
        tmpfile.write ( qsubfile )
        filename = tmpfile.name
        tmpfile.close ()

        self.current.processfile ( filename, printfile = False )
        self.assertEqual ( self.current.attr ['queue'], "standby" )
        self.assertEqual ( self.current.attr ['nodes'], "1" )
        self.assertTrue ( "module" in self.current.comm [0:][0] )
        os.unlink ( filename )
        
    def test_identical_output ( self ):
        qsubfile = "#!/bin/sh\n#PBS -l nodes=1:ppn=3,pvmem=5GB\n" +  \
            "#PBS -q standby\nmodule load mpi/openmpi/1.6.5\n" +  \
            "echo Hello"

        # Create sample submission script ; and capture output
        tmpfile = tempfile.NamedTemporaryFile ( mode = 'w', delete = False )
        tmpfile.write ( qsubfile )
        filename = tmpfile.name
        tmpfile.close ()
        
        expect_tmp = tempfile.NamedTemporaryFile ( mode = 'w', delete = False )
        tmpoutfile = expect_tmp.name
        expect_tmp.close ()

        # Submit file into processfile () - writing STDOUT to tmpoutfile
        self.current.processfile ( filename, outfile = tmpoutfile )
        shellcmd = ['cmp', filename, tmpoutfile]
        self.assertEqual ( subprocess.call ( shellcmd ), 0 )
      
        os.unlink ( filename )
        os.unlink ( tmpoutfile )
        
if __name__ == '__main__':
    unittest.main()
