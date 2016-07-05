
#!/bin/env python
# Test torquefilter class


import os.path, sys
import unittest

import torquefilter
from torquefilter.queue.queue import queue

class TestTorqueFilterMethods ( unittest.TestCase ):
    "Test submitfilter main methods"

    def setUp(self):
        self.current = queue()

    def test_addName(self):
        """ Check queue class can accept queue names. """

        self.current.addName('comm_mmem_day')
        self.assertEqual(self.current.name, 'comm_mmem_day')

    def test_addMemLimit(self):
        """ Check that queue class memory limits can be added. """

        self.current.addMemLimit(54)
        self.assertEqual(self.current.memLimit, 54)


if __name__ == '__main__':
    unittest.main()

