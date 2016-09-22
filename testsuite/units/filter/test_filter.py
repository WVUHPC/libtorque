
#!/bin/env python

import unittest

from torquefilter.exceptions.error import illegalMemConfig
from torquefilter.exceptions.error import illegalCommand
from torquefilter.exceptions.error import illegalConfig

from torquefilter.filter.queue.queue import queue
from torquefilter.filter.subfilter import subfilter


class sampleMap:
    """Small sample class to hold attributes and commands."""

    def __init__(self):
        self.attributes = {}
        self.commands   = []

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def addCommand(self, comm):
        self.commands.append(comm)

    def getCommands(self):
        return self.commands

    def getAttributes(self):
        return self.attributes


class TestFilterClass(unittest.TestCase):
    """ Test filter class """

    def test_simpleCall(self):
        """Test that filter class is callable."""

        self.current = subfilter()

    def test_illMemConfig(self):
        """Test that filter class catches illegal memory configuration."""

        queueList = []
        queueList.append(queue('medium_day', 54))
        queueList.append(queue('medium_week', 54))

        # Setup that uses 160gb of memory on a 54gb queue class
        sample = sampleMap()
        sample.addAttribute('destination', 'medium_day')
        sample.addAttribute('pvmem', '10gb')
        sample.addAttribute('ppn', 16)

        self.assertRaises(illegalMemConfig, subfilter, queueList, sample)

    def test_illCommand(self):
        """Test filter class catches illegal commands."""

        illegalCommands = ['ssh']

        commandList = sampleMap()
        commandList.addCommand(['ssh', 'server6'])

        self.assertRaises(illegalCommand, subfilter, values=commandList, 
                commands=illegalCommands)


    def test_illegalConfig(self):
        """Test filter class catches illegal qsub attributes."""
        
        illegalAttributes = ['mem']

        sample = sampleMap()
        sample.addAttribute('mem', '10gb')

        self.assertRaises(illegalConfig, subfilter, values=sample, attributes=illegalAttributes)


if __name__ == '__main__':
    unittest.main()
