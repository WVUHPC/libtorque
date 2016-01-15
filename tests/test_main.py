
#!/bin/env python
# Test torque_submitfilter exit status under varying conditions


import os.path, sys, subprocess
import unittest

class TestMain ( unittest.TestCase ):
    "Test submitfilter exit status"

    def setUp ( self ):
        self.comm = ["../libtorque/torque_submitfilter.py"]

    def test_working ( self ):
        """ working.pbs gives a zero exit status """
        self.comm.append ( "pbsfiles/working.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 0 )

    def test_illegal_comm ( self ):
        """ illegalcomm.pbs gives a -1 exit status """
        self.comm.append ( "pbsfiles/illegalcomm.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )

    def test_illegal_memattr ( self ):
        """ illegalattr.pbs gives a -1 exit status """
        self.comm.append ( "pbsfiles/illegalattr.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )

    def test_illegal_req ( self ):
        """ illegalreq.pbs gives a -1 exit status """
        self.comm.append ( "pbsfiles/illegalreq.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )

    def test_illegal_ppn ( self ):
        """ illegalppn.pbs gives a 1 exit status """
        self.comm.append ( "pbsfiles/illegalppn.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )

    def test_multiple_files ( self ):
        """ multiple files should give a -1 exit status """
        self.comm.append ( "pbsfiles/working.pbs" )
        self.comm.append ( "pbsfiles/illegalcomm.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )

    def test_invalid_options ( self ):
        """ invalid options gives a -1 exit status """
        self.comm.append ( "-g" )
        self.comm.append ( "pbsfiles/working.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 2 )

    def test_incorrect_file ( self ):
        """ incorrect file name gives a -1 exit status """
        self.comm.append ( "pbsfiles/doesnotexit.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 1 )


if __name__ == '__main__':
    unittest.main()

