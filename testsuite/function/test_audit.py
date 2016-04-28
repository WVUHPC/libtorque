
#!/bin/env python
# Test torque_submitfilter exit status under varying conditions


import os.path, sys, subprocess
import unittest
import tempfile, json

class TestMain ( unittest.TestCase ):
    "Test submitfilter exit status"

    def _runCommand(self):

        filterRun = subprocess.Popen(self.comm, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
        filterRun.wait()
        return filterRun.returncode

    def setUp ( self ):
        self.path = os.path.dirname ( os.path.realpath ( __file__ ) )
        command = self.path + "/scripts/audit.py"
        self.comm = [command]

        tmpfile = tempfile.NamedTemporaryFile ( mode = 'w', delete=False )
        self.tmpfile = tmpfile.name
        tmpfile.close ()

    def tearDown ( self ):
        os.unlink ( self.tmpfile )

    def test_working_audit ( self ):
        """ Audit working.pbs """
        self.comm.append ( self.path + "/pbsfiles/working.pbs" )
        self.comm.append ( self.tmpfile )
        exit_code = self._runCommand()
        self.assertEqual ( exit_code, 0 )

        # Check tmpfile for correct JSON structures
        current = open ( self.tmpfile )
        decoder = json.JSONDecoder ()
        jsonData = decoder.decode ( json.load ( current ) )

        self.assertEqual ( jsonData ['Commands'][0][0], 'mpirun' )
        self.assertEqual ( jsonData ['mpirun'][0]['-np'], '16' )
        self.assertEqual ( jsonData ['mpirun'][0]['-host'], '$PBS_NODEFILE' )
        self.assertEqual ( jsonData ['queue'], 'comm_mmem_day' )

        current.close ()

    def test_module_audit ( self ):
        """ Audit moduleload.pbs """
        self.comm.append ( self.path + "/pbsfiles/moduleload.pbs" )
        self.comm.append ( self.tmpfile )
        exit_code = self._runCommand()
        self.assertEqual ( exit_code, 0 )

        # Pull Json structure
        current = open ( self.tmpfile )
        decoder = json.JSONDecoder ()

        jsonData = decoder.decode ( json.load ( current ) )

        # Check JSON data ( python dictionary )
        self.assertEqual ( jsonData ['Commands'][0][0], 'mpirun' )
        self.assertEqual ( jsonData ['mpirun'][0]['-np'], '16' )
        self.assertEqual ( jsonData ['queue'], 'comm_mmem_day' )

        self.assertEqual ( jsonData ['Commands'][1][0], 'module' )
        self.assertEqual ( jsonData ['Loaded Modules'][0], \
                                    ['module1', 'module2', 'module3'] )

        current.close ()


if __name__ == '__main__':
    unittest.main()

