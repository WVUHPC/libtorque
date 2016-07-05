
class queue:
    """ Class defining queue class attributes.

    *name*          -   String containing queue class name.
    *memLimit*      -   Integer specifying memory limit of queue class nodes.
    """

    def __init__(self, name=None, memLimit=None):

        self.name       =   name
        self.memLimit   =   memLimit

    def addName(self, name):
        """ Add name to queue class attributes. """

        self.name = name

    def addMemLimit(self, memLimit):
        """ Add memory limit to queue class attributes. """

        self.memLimit   =   memLimit

