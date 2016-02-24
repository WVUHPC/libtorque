
#!/bin/env python
# Test torquefilter class


import os.path, sys
import unittest

import torquefilter
from torquefilter.error import illegalMemReq, illegalCommand
from torquefilter.error import illegalConfig, illegalMemConfig

class TestTorqueFilterMethods ( unittest.TestCase ):
    "Test submitfilter main methods"

    def setUp ( self ):
        self.current = torquefilter.torqueFilter () 

    def test_rtn_filename ( self ):
        sys.argv = []
        self.current.rtn_filename ()
        self.assertEqual ( self.current.filename, "STDIN" )
        sys.argv = ( "filename -l nodes=1 pbsfile.sh".split () )
        self.current.rtn_filename ()
        self.assertEqual ( self.current.filename, "pbsfile.sh" )

    def test_checkQueue ( self ):
        self.current.checkQueue ( ['comm_mmem_week'] )
        self.assertEqual ( self.current.queuesToCheck, ['comm_mmem_week'] )

    def test_illComm ( self ):
        self.current.illComm ( ['ssh'] )
        self.assertEqual ( self.current.commandsToCheck, ['ssh'] )

    def test_illAttr ( self ):
        self.current.illAttr ( ['vmem'] )
        self.assertEqual ( self.current.attrToCheck, ( ['vmem'] ) )

    def test_chk_memory_attributes ( self ):
        attr = { }
        attr ['queue'] = "comm_mmem_week"
        attr ['pvmem'] = "7GB"
        attr ['ppn'] = "15"
        self.current.add_attr ( attr )
        self.current.checkQueue ( ['comm_mmem_week'] )
        self.assertRaises ( illegalMemConfig, self.current.chk_memory )

    def test_chk_ppn ( self ):
        attr = { }
        attr ['queue'] = "comm_mmem_week"
        attr ['ppn'] = "19"
        self.current.add_attr ( attr )
        self.current.checkQueue ( ['comm_mmem_week'] )
        self.assertRaises ( illegalConfig, self.current.chk_memory )

    def test_chk_memory_resources ( self ):
        attr = { }
        attr ['queue'] = "comm_mmem_week"
        attr ['vmem'] = "32mb"
        self.current.add_attr ( attr )
        self.current.illAttr ( ['vmem'] )
        self.assertRaises ( illegalMemReq, self.current.chk_attr )

    def test_chk_memory_good ( self ):
        attr = { }
        attr ['ppn'] = "4"
        attr ['pvmem'] = "3GB"
        self.current.add_attr ( attr )
        self.current.checkQueue ( ['comm_mmem_week'] )
        self.assertEqual ( self.current.chk_memory (), True )

    def test_chk_commands ( self ):
        self.current.add_command ( "qsub submitfile.sh" )
        self.current.illComm ( ['qsub'] )
        self.assertRaises ( illegalCommand, self.current.chk_commands )



if __name__ == '__main__':
    unittest.main()

