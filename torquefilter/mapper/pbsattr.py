
class PBSattr:
    "Dictionary structure for job commands/attirbutes"

    def __init__(self):
        self.attr       =   {}
        self.comm       =   []

    def __chk_duplicate(self, attr):
        """Check if attr is already defined
        
        Used to avoid overwrite of attributes if not desired
        """

        if (attr in self.attr):
            return False
        else:
            return True

    def add_attribute(self, attr_map, overWrite=False):
        """Add PBS attribute and value to global attributes"""

        for key in iter(attr_map):
            if (not overWrite):
                if (self.__chk_duplicate(key)):
                    self.attr[key] = attr_map[key]
            else:
                self.attr[key] = attr_map[key]


    def add_command(self, command):
        "Add commands to command list"

        self.comm.append(command.split())
