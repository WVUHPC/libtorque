
class PBSattr:
    "Dictionary structure for job commands/attirbutes"

    def __init__(self):
        self.attributes         =   {}
        self.commands           =   []

    def __chk_duplicate(self, attr):
        """Check if attr is already defined
        
        Used to avoid overwrite of attributes if not desired
        """

        if (attr in self.attributes):
            return False
        else:
            return True

    def add_attribute(self, attr_map, overWrite=False):
        """Add PBS attribute and value to global attributes"""

        for key in iter(attr_map):
            if (not overWrite):
                if (self.__chk_duplicate(key)):
                    self.attributes[key] = attr_map[key]
            else:
                self.attributes[key] = attr_map[key]


    def add_command(self, command):
        "Add commands to command list"

        self.commands.append(command.split())
