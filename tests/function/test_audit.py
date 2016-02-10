
#!/bin/env python
# Test torque_submitfilter exit status under varying conditions


import os.path, sys, subprocess
import unittest
import tempfile, json

class TestMain ( unittest.TestCase ):
    "Test submitfilter exit status"

    def setUp ( self ):
        self.path = os.path.dirname ( os.path.realpath ( __file__ ) )
        command = self.path + "/scripts/audit.py"
        self.comm = [command]

        tmpfile = tempfile.NamedTemporaryFile ( mode 'w', delete=False )
        self.tmpfile = tmpfile.name
        tmpfile.close ()

    def tearDown ( self ):
        self.tmpfile.close ()
        os.unlink ( self.tmpfile )

    def test_working_audit ( self ):
        """ working.pbs gives a zero exit status """
        self.comm.append ( self.path + self.tmpfile + "/pbsfiles/working.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 0 )

        # Check tmpfile for correct JSON structures
        current = open ( self.tmpfile )
        decoder = json.JSONDecoder ()
        jsonData = decoder ( json.load ( current ) )

        self.assertEqual ( jsonData ['Commands'][0], 'mpirun' )
        self.assertEqual ( jsonData ['mpirun']['-np'], '16' )
        self.assertEqual ( jsonData ['mpirun']['-host'], '$PBS_NODEFILE' )
        self.assertEqual ( jsonData ['queue'], 'comm_mmem_day' )

    def test_module_audit ( self ):
        """ illegalcomm.pbs gives a -1 exit status """
        self.comm.append ( self.path + self.tmpfile + "/pbsfiles/moduleload.pbs" )
        exit_code = subprocess.call ( self.comm )
        self.assertEqual ( exit_code, 0 )

        # Pull Json structure
        current = open ( self.tmpfile )
        decoder = json.JSONDecoder ()

        jsonData = decoder ( json.load ( current ) )

        # Check JSON data ( python dictionary )
        self.assertEqual ( jsonData ['Commands'][0], 'mpirun' )
        self.assertEqual ( jsonData ['mpirun']['-np'], '16' )
        self.assertEqual ( jsonData ['mpirun']['-host'], '$PBS_NODEFILE' )
        self.assertEqual ( jsonData ['queue'], 'comm_mmem_day' )

        self.assertEqual ( jsonData ['Module Loads'][0], 'module' )
        self.assertEqual ( jsonData ['Loaded Modules'][0], 'module1' )
        self.assertEqual ( jsonData ['Loaded Modules'][1], 'module2' )
        self.assertEqual ( jsonData ['Loaded Modules'][2], 'module3' )


if __name__ == '__main__':
    unittest.main()

