# User-defined Exceptions for libtorque python library

class Error ( Exception ):
    """ Base class for exceptions in libtorque module. """
    pass

class illegalMemReq ( Error ):
    """ 
    Raised for illegal memory attributes within PBS. 
    """

class illegalMemConfig ( Error ):
    """ 
    Raised for illegal memory request.  Specifically, if too much memory was
    requested over limit for queue class

    Several internal members are assigned to certain class variables when
    instance is called:

    *totalMem*  - The amount of total memory requested
    *queue*     - The queue class requested
    *pvmem*     - The amount of memory per CPU
    *availMem*  - Configured memory limit for reqeusted queue class
    """

    def __init__ ( self, totalMem, queue, pvmem, availMem ): 
        self.totalMem   =       str ( totalMem )
        self.queue      =       queue
        self.pvmem      =       str ( pvmem )
        self.availMem   =       str ( availMem )
        
class illegalCommand ( Error ):
    """ 
    Raised for illegal command rule violation. 

    *cmd*       - Specific command that raised exception
    """

    def __init__ ( self, cmd ):
        self.cmd = cmd

class illegalConfig ( Error ):
    """ 
    Raised for illegal PBS attribute rule violation.

    *attr*      - Specific attribute that raised exception
    """

    def __init__ ( self, attr ):
        self.attr       =       attr
