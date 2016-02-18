
#!/bin/env python
# Test torque_submitfilter


import os, sys, fnmatch
import sqlite3, tempfile
import unittest

from torquefilter import audit
from torquefilter.qsub.pbsattr import PBSattr


class TestMainMethods ( unittest.TestCase ):
    "Test jobauditer methods"

    def setUp ( self ):
        jobParameters = PBSattr ()

        jobParameters.comm.append ( "mpirun -np 16 fake.exe".split () )
        jobParameters.comm.append ( \
                    "module load module1 module2 module3".split () )
        jobParameters.attr ['queue'] = 'comm_mmem_day'

        self.tellme = audit.jobauditer ( jobParameters )


    def test_instance ( self ):
        """Verify jobParameters are inserted into class instance"""

        self.assertEqual ( self.tellme.attributes ['queue'], 'comm_mmem_day' )
        self.assertEqual ( self.tellme.commands [0], \
                                ['mpirun', '-np', '16', 'fake.exe' ] )

 
    def test_init ( self ):
        """ Verify correct output setup """

        # init () should place all tmp files in a given directory, output to a
        # specify given file, or output to TMPDIR

        self.tellme.init ()

        dirName = tempfile.gettempdir ()
        prefix = tempfile.gettempprefix ()

        mstring = dirName + '/' + prefix + '*'
        self.assertTrue ( fnmatch.fnmatch ( self.tellme.fileName,  mstring ) )

        os.unlink ( self.tellme.fileName )

        # Given a directory
        dirName = tempfile.mkdtemp ()

        self.tellme.init ( dirName )

        mstring = dirName + '/' + prefix + '*'
        self.assertTrue ( fnmatch.fnmatch ( self.tellme.fileName, mstring ) )

        os.unlink ( self.tellme.fileName )
        os.rmdir ( dirName )

        # Given a file
        current = tempfile.NamedTemporaryFile ( mode='w', delete=False )
        current.close ()
        self.tellme.init ( current.name )

        self.assertEqual ( self.tellme.fileName, current.name )

        os.unlink ( self.tellme.fileName )

    def test_command ( self ):
        """ Verify insertion of JSON structure for command () """

        self.tellme.command ( 'mpirun' )

        self.assertEqual ( self.tellme.jsonData ['Commands'][0][0], 'mpirun' )

    def test_commandArgs ( self ):
        """ Verify insertion of JSON structure for commandArgs () """

        self.tellme.commandArgs ( 'mpirun', ['-np'], 'Parallel Job Scale' )

        self.assertTrue ( 'Parallel Job Scale' in self.tellme.jsonData )
        self.assertTrue ( '-np' in self.tellme.jsonData ['Parallel Job Scale'][0] )
        self.assertEqual ( self.tellme.jsonData \
                            ['Parallel Job Scale'][0]['-np'], '16' )

    def test_commandSlice ( self ):
        """ Verify insertion of JSON structure for commandSlice () """

        self.tellme.commandSlice ( 'module', ['load'], \
                        start=2, tableName = 'Loaded Modules' )

        self.assertTrue ( 'Loaded Modules' in self.tellme.jsonData )
        self.assertEqual ( self.tellme.jsonData ['Loaded Modules'][0], \
                                    ['module1', 'module2', 'module3'] )
        

    def test_attr ( self ):
        """ Verify insertion of JSON structure for attr () """

        self.tellme.attr ( 'queue' )

        self.assertEqual ( self.tellme.jsonData ['queue'], 'comm_mmem_day' )


if __name__ == '__main__':
    unittest.main()

