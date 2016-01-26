import sys

class PBSattr:
    "Class for PBS attribute totals for a single job"

    def __init__ (self):
        self.attr       =   { }
        self.comm       =   [ ]
        self.attr ['Interactive'] = False

    def __chk_duplicate (self, attr):
        "Check if attr is already defined"

        if (attr in self.attr):
            return False
        else:
            return True

    def add_attr (self, attr_map, overWrite=False):
        """Add PBS attribute and value to global attributes"""

        for key in iter (attr_map):
            if (not overWrite):
                if (self.__chk_duplicate (key)):
                    self.attr [key] = attr_map [key]
            else:
                self.attr [key] = attr_map [key]


    def add_command (self, command):
        "Add commands to command list"

        self.comm.append (command.split ())
