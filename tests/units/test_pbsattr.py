
#!/bin/env python
# Test Qsubfile Class


import os.path, sys
import unittest

from torquefilter.qsub.pbsattr import PBSattr


class TestpbsattrMethods (unittest.TestCase):
    "Test pbsattr class methods"

    def setUp (self):
        self.current = PBSattr ()

    def test_add_attr (self):
        map_attr = { }
        map_attr ['queue'] = "standby"
        self.current.add_attr (map_attr)
        self.assertEqual (self.current.attr ['queue'], "standby")
   
    def test_duplicates (self):
        map_attr = { }
        second_attr = { }
        map_attr ['queue'] = "standby"
        second_attr ['queue'] = "comm_mmem_week"
        self.current.add_attr (map_attr)
        self.current.add_attr (second_attr)
        self.assertEqual (self.current.attr['queue'], "standby")

    def test_overwrite (self):
        map_attr = { }
        second_attr = { }
        map_attr ['queue'] = "standby"
        second_attr ['queue'] = "comm_mmem_week"
        self.current.add_attr (map_attr)
        self.current.add_attr (second_attr, overWrite=True)
        self.assertEqual (self.current.attr['queue'], "comm_mmem_week")

    def test_add_multiple_attr (self):
        map_attr = { }
        map_attr ['queue'] = "standby"
        map_attr ['nodes'] = "1"
        map_attr ['pvmem'] = "5GB"
        map_attr ['ppn'] = "1"
        self.current.add_attr (map_attr)
        self.assertEqual (self.current.attr ['pvmem'], "5GB")
        self.assertEqual (self.current.attr ['nodes'], "1")

    def test_add_command (self):
        self.current.add_command ("ssh srih0001")
        self.assertEqual (['ssh', 'srih0001'], self.current.comm [0])

    def test_self_comm (self):
        self.current.add_command ("ssh srih0001")
        self.current.add_command ("qsub -N file")
        self.assertEqual (self.current.comm [1], ['qsub', '-N', 'file'])
        self.assertEqual (self.current.comm [1][0], 'qsub')
        

if __name__ == '__main__':
    unittest.main()
