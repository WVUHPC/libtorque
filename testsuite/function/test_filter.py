
#!/bin/env python
# Test torque_submitfilter exit status under varying conditions


import os.path, sys, subprocess
import unittest



class TestMain(unittest.TestCase):
    "Test submitfilter exit status"

    def _runCommand(self):

        filterRun = subprocess.Popen(self.comm, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
        filterRun.wait()
        return filterRun.returncode

    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        command = self.path + "/scripts/filter.py"
        self.comm = [command]

    def test_working(self):
        """ working.pbs gives a zero exit status """
        self.comm.append(self.path + "/pbsfiles/working.pbs")

        exit_code = self._runCommand()
        self.assertEqual(exit_code, 0)

    def test_illegal_comm(self):
        """ illegalcomm.pbs gives a 1 exit status """
        self.comm.append(self.path + "/pbsfiles/illegalcomm.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)

    def test_illegal_memattr(self):
        """ illegalattr.pbs gives a 1 exit status """
        self.comm.append(self.path + "/pbsfiles/illegalattr.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)

    def test_illegal_req(self):
        """ illegalreq.pbs gives a 1 exit status """
        self.comm.append(self.path + "/pbsfiles/illegalreq.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)

    def test_multiple_files(self):
        """ multiple files should give a 1 exit status """
        self.comm.append(self.path + "/pbsfiles/illegalcomm.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)

    def test_invalid_options(self):
        """ invalid options gives a 1 exit status """
        self.comm.append("-g")
        self.comm.append(self.path + "/pbsfiles/working.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)

    def test_incorrect_file(self):
        """ incorrect file name gives a 1 exit status """
        self.comm.append(self.path + "/pbsfiles/doesnotexist.pbs")
        exit_code = self._runCommand()
        self.assertEqual(exit_code, 1)


if __name__ == '__main__':
    unittest.main()

