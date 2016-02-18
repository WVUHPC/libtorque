
#!/bin/env python

import unittest

from torquefilter import audit
from torquefilter.qsub.pbsattr import PBSattr

class TestPrivateMethods ( unittest.TestCase ):
    """ Test jobauditer 'private' methods """

    def setUp ( self ):
        jobParameters = PBSattr ()

        self.instance = audit.jobauditer ( jobParameters )

    def test_tableMethods ( self ):
        """ Test _checkTable and _writeTable methods """

        self.instance._checkTable ( 'Commands' )

        self.assertTrue ( 'Commands' in self.instance.jsonData )

        self.instance._writeTable ( 'Commands', ['module1', 'module2'] )

        self.assertEqual ( self.instance.jsonData ['Commands'][0], \
                                        ['module1', 'module2'] )

    def test_checkArgs ( self ):
        """ Test _checkArgs method """

        cmd = "module load module1 module2 module3".split ()

        args1 = ['load']
        args2 = ['notreal']

        self.assertTrue ( self.instance._checkArgs ( cmd, args1 ) )
        self.assertFalse ( self.instance._checkArgs ( cmd, args2 ) )

    def test_listToDict ( self ):
        """ Test _listToDict method """

        arry=  "-arg1 15 -arg2 30 -arg3".split ()

        newDict = self.instance._listToDict ( arry )

        self.assertEqual ( newDict ['-arg1'], '15' )
        self.assertEqual ( newDict ['-arg2'], '30' )
        self.assertEqual ( newDict ['-arg3'], True )

    def test_captureArgs ( self ):
        
        args = "-arg1 -arg3".split ()

        cmd = "fakeCmd -arg1 15 -arg2 10 -arg3".split ()

        newDict = self.instance._captureArgs ( cmd, args )

        self.assertEqual ( newDict ['-arg1'], '15' )
        self.assertEqual ( newDict ['-arg3'], True )
        self.assertFalse ( '-arg2' in newDict ) 


if __name__ == '__main__':
    unittest.main()
