
#!/bin/env python
# Test torque_submitfilter


import os.path, sys
import unittest

from libtorque.qsub_error import illegalMemReq, illegalMemAttributes, illegalCommand
from torque_submitfilter import rtn_filename, chk_memory, chk_commands
from libtorque.qsubfile import qsubfile


class TestMainMethods ( unittest.TestCase ):
    "Test submitfilter main methods"

    def test_rtn_filename ( self ):
        current = qsubfile ()
        sys.argv = []
        self.assertEqual ( rtn_filename (current), "STDIN" )
        sys.argv = ( "filename -l nodes=1 pbsfile.sh".split () )
        self.assertEqual ( rtn_filename (current), "pbsfile.sh" )

    def test_chk_memory_attributes ( self ):
        attr = { }
        attr ['queue'] = "comm_mmem_week"
        attr ['pvmem'] = "7GB"
        attr ['ppn'] = "15"
        self.assertRaises ( illegalMemAttributes, chk_memory, attr )


    def test_chk_memory_resources ( self ):
        attr = { }
        attr ['queue'] = "comm_mmem_week"
        attr ['vmem'] = "32mb"
        self.assertRaises ( illegalMemReq, chk_memory, attr )

    def test_chk_memory_good ( self ):
        attr = { }
        attr ['ppn'] = "4"
        attr ['pvmem'] = "3GB"
        self.assertEqual ( chk_memory (attr), True )

    def test_chk_commands ( self ):
        comm = [ ]
        comm.append ( "qsub submitfile.sh".split () )
        self.assertRaises ( illegalCommand, chk_commands, comm )



if __name__ == '__main__':
    unittest.main()

