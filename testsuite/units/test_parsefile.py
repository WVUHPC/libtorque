#!/bin/env python
# Test Qsubfile Class


import os.path, sys
import tempfile
import subprocess

import unittest

from torquefilter.qsub.parser import processfile

class attribute_map:

    def __init__(self):
        self.attr = { }
        self.comm = [ ]

    def add_command(self, command):
        
        self.comm.append(command)

    def add_directive(self, attribute):
        
        self.attr[attribute[0]] = attribute[1]
        

class TestProcessFile (unittest.TestCase):
    "Test ProcessFile class methods"

    def setUp (self):
        self.current = processfile(attribute_map)

    def test_strip_command (self):
        command = "<file1 qsub -N file >>output.txt"
        self.assertEqual (self.current.parse_comm (command), ['qsub -N file']) 

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
        "Check for identical output"
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
