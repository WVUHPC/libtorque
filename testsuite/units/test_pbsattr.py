
#!/bin/env python
# Test PBSattr Class


import os.path
import sys
import unittest

from torquefilter.mapper.pbsattr import PBSattr

class Test_PBS_map(unittest.TestCase):

    def setUp(self):
        self.current = PBSattr()

    def test_map_attribute(self):
        "Check that attributes can be mapped"

        map_attr = {}
        map_attr['queue'] = "standby"
        self.current.add_attribute(map_attr)
        self.assertEqual(self.current.attr['queue'], "standby")

    def test_no_overwrite_attribute(self):
        "Check that duplicates do not overwrite initial attribute by default"

        map_attr = {}
        second_attr = {}
        map_attr['queue'] = "standby"
        second_attr['queue'] = "comm_mmem_week"
        self.current.add_attribute(map_attr)
        self.current.add_attribute(second_attr)
        self.assertEqual(self.current.attr['queue'], "standby")

    def test_overwrite_attribute(self):
        "Check that duplicates overwrite initial attribute if configured"

        map_attr = {}
        second_attr = {}
        map_attr['queue'] = "standby"
        second_attr['queue'] = "comm_mmem_week"
        self.current.add_attribute(map_attr)
        self.current.add_attribute(second_attr, overWrite=True)
        self.assertEqual(self.current.attr['queue'], "comm_mmem_week")

    def test_map_multiple_attribute(self):
        "Check that multiple attributes can be mapped at the same time"

        map_attr = {}
        map_attr['queue'] = "standby"
        map_attr['nodes'] = "1"
        map_attr['pvmem'] = "5GB"
        map_attr['ppn'] = "1"
        self.current.add_attribute(map_attr)
        self.assertEqual(self.current.attr['pvmem'], "5GB")
        self.assertEqual(self.current.attr['nodes'], "1")

    def test_map_command(self):
        "Check that commands can be mapped"

        self.current.add_command("ssh srih0001")
        self.assertEqual(['ssh', 'srih0001'], self.current.comm[0])

    def test_command_index(self):
        "Check that we can reference specific indexes of mapped commands"

        self.current.add_command("ssh srih0001")
        self.current.add_command("qsub -N file")
        self.assertEqual(self.current.comm[1], ['qsub', '-N', 'file'])
        self.assertEqual(self.current.comm[1][0], 'qsub')
        

if __name__ == '__main__':
    unittest.main()
