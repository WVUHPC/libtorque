
#!/bin/env python
# Test torque_submitfilter


import os, sys
import sqlite3, tempfile
import unittest

from torquefilter.audit.condense_audit import hashadd, hash_from_file, ins_hash_sqlite
from torquefilter.audit.condense_audit import rtn_epoch, create_table

class TestMainMethods ( unittest.TestCase ):
    "Test submitfilter main methods"

    def test_hashadd ( self ):
        self.hash1 = { }
        self.hash2 = { }
        self.hash1 ['first'] = 5
        self.hash1 ['second'] = 10
        self.hash2 ['first'] = 4
        self.hash2 ['second'] = 9
        self.hash2 ['third'] = 11
        self.hash1 = hashadd ( self.hash1, self.hash2 )
        self.assertEqual ( self.hash1 ['first'], 9 )
        self.assertEqual ( self.hash1 ['second'], 19 )
        self.assertEqual ( self.hash1 ['third'], 11 )

    def test_filehash ( self ):
        # Create a tmp file
        content = "genomics/samtools\nboost/1.55.0\n"
        tmpfile = tempfile.NamedTemporaryFile ( mode = 'w', delete = False )
        tmpfile.write ( content )
        filename = tmpfile.name
        tmpfile.close ()

        # Run test
        self.hash = hash_from_file ( filename )
        self.assertEqual ( self.hash ['genomics/samtools'], 1 )
        self.assertEqual ( self.hash ['boost/1.55.0'], 1 )

        os.unlink ( filename )

    def test_ins_hash_sqlite ( self ):
        # Create hash
        hash = { }
        hash ['genomics/samtools'] = 2
        hash ['boost/1.55.0'] = 5
        hash ['filenum'] = 3
        hash ['loadnum'] = 2
        
        tmpfile = tempfile.NamedTemporaryFile ( mode = "w", delete = False )
        filename = tmpfile.name
        tmpfile.close ()
        create_table ( filename )
        ins_hash_sqlite ( filename , hash, rtn_epoch () )

        # Check sqlite values
        conn = sqlite3.connect ( filename )
        c = conn.cursor ()

        # Test sqlite3 values
        row = c.execute ( 'SELECT * FROM ledger' )
        values = row.fetchone ()
        self.assertEqual ( values [ 1 ], 3 )
        self.assertEqual ( values [ 2 ], 2 )


        for row in c.execute ( 'SELECT * FROM modules' ):
            key = row [ 0 ]
            self.assertEqual ( row [ 1 ], hash [ key ] )

        conn.close ()
        os.unlink ( filename )

if __name__ == '__main__':
    unittest.main()

