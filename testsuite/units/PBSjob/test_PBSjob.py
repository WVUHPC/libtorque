#/bin/env python
# Test Qsubfile Class


import unittest
import tempfile
import os

from torquefilter.PBSjob.pbsjob import PBSjob

class TestPBSjob(unittest.TestCase):
    """ Test PBSjob class """

    def test_instance(self):
        "Check that PBSjob can be initialized"

        args = "qsub -l nodes=1:ppn=3,pvmem=5GB -q standby -I".split ()

        current = PBSjob(args)

        self.assertEqual(current.filename, 'STDIN')
        self.assertEqual(current.mapper.attributes['destination'], ['standby'])


    def test_parsefile(self):
        "Check that PBSjob can handle PBS files"

        qsubfile = "#!/bin/sh\n#PBS -q standby\n" \
            + "module load mpi/openmpi/1.6.5\n" \
            + "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        args = ['qsub', filename]

        current = PBSjob(args)

        self.assertEqual(current.filename, filename)
        self.assertEqual(current.mapper.attributes['destination'], ['standby'])
        self.assertTrue("module" in current.mapper.commands[0:][0])
        os.unlink(filename)

    def test_getCommand(self):
        "Check that PBSjob can return commands from submit file"

        qsubfile = "#!/bin/sh\n#PBS -q standby\n" \
            + "module load mpi/openmpi/1.6.5\n" \
            + "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        args = ['qsub', filename]

        current = PBSjob(args)

        against = current.getCommands()
        
        self.assertTrue("module" in against[0:][0])
        os.unlink(filename)


    def test_getAttributes(self):
        "Check that PBSjob can return attributes from submit file"
        
        qsubfile = "#!/bin/sh\n#PBS -q standby\n" \
            + "module load mpi/openmpi/1.6.5\n" \
            + "echo Hello"

        # Create sample submission script
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile.write(qsubfile)
        filename = tmpfile.name
        tmpfile.close()

        args = ['qsub', filename]

        current = PBSjob(args)

        against = current.getAttributes()

        self.assertEqual(against['destination'], ['standby'])
        os.unlink(filename)


if __name__ == '__main__':
    unittest.main()
