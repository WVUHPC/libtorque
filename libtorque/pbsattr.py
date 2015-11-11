import sys

class PBSattr:
    "Class for PBS attribute totals for a single job"

    def __init__ (self):
        self.attr       =   { }
        self.comm       =   [ ]
        self.num_com    =   0
        self.attr ['Interactive'] = False

    def __chk_duplicate (self, attr):
        "Check if attr is already defined"

        if (attr in self.attr):
            sys.stderr.write ("PBS directive duplication: %s \n" % attr)
            return False
        else:
            return True

    def add_attr (self, attr_map):
        """Add PBS attribute and value to global attributes"""

        for key in iter (attr_map):
            if (self.__chk_duplicate (key)):
                self.attr [key] = attr_map [key]


    def add_command (self, command):
        "Add commands to command list"

        self.comm.append (command.split ())
