
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

    def __resources(self, resource_attributes):
        """Parse resources list into direct mappable units"""

        tmp_attr = {}

        for attr in resource_attributes:
            # Parse resource into mapping attribute
            # attr should be a list with a single string
            for each in attr[0].split(','):
                # Add extra split for nodes resource and it's respective 
                # properties
                if 'nodes' in each:
                    for param in each.split(':'):
                        if ('=' in param):
                            keyword, value = param.split('=')
                            tmp_attr[keyword] = value
                        else:
                            tmp_attr[param] = True
                else:
                    # All other resources
                    if ('=' in each):
                        keyword, value = each.split('=')
                        tmp_attr[keyword] = value
                    else:
                        tmp_attr[each] = True

        return tmp_attr

    def add_attribute(self, attr_map, overWrite=False):
        """Add PBS attribute and value to global attributes"""

        # Add direct resource list mappings
        if 'resource_list' in attr_map:
            self.add_attribute(self.__resources(attr_map['resource_list']))

        for key in iter(attr_map):
            if (not overWrite):
                if (self.__chk_duplicate(key)):
                    self.attributes[key] = attr_map[key]
            else:
                self.attributes[key] = attr_map[key]


    def add_command(self, command):
        "Add commands to command list"

        self.commands.append(command.split())
