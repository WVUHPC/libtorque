
#!/bin/env python
# Test torquefilter class


import os.path, sys
import unittest

import torquefilter
from torquefilter.filter.queue.queue import queue

class TestQueueClass(unittest.TestCase):
    "Test submitfilter main methods"

    def test_addName(self):
        """ Check queue class can accept queue names. """

        self.current = queue()
        self.current.addName('comm_mmem_day')
        self.assertEqual(self.current.name, 'comm_mmem_day')

    def test_addMemLimit(self):
        """ Check that queue class memory limits can be added. """

        self.current = queue()
        self.current.addMemLimit(54)
        self.assertEqual(self.current.memLimit, 54)

    def test_multipleQueues(self):
        """ Check that queues can be kept in lists. """

        queues = []
        queues.append(queue('comm_mmem_day', 54))
        queues.append(queue('comm_mmem_week', 54))

        self.assertEqual(len(queues), 2)
        self.assertEqual(queues[0].name, 'comm_mmem_day')
        self.assertEqual(queues[1].memLimit, 54)

if __name__ == '__main__':
    unittest.main()

