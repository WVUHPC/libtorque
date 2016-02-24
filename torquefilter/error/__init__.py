# User-defined Exceptions for libtorque python library

class Error ( Exception ):
    """ Base class for exceptions in libtorque module. """
    pass

class illegalMemReq ( Error ):
    """ Exception raised for illegal memory attributes within PBS. """

class illegalMemConfig ( Error ):
    """ Exception raised for setting memory attributes greater than memory
    resources. """

    def __init__ ( self, totalMem, queue, pvmem, availMem ): 
        self.totalMem   =       str ( totalMem )
        self.queue      =       queue
        self.pvmem      =       str ( pvmem )
        self.availMem   =       str ( availMem )
        
class illegalCommand ( Error ):
    """ Exception raised for using illegal commands. """

    def __init__ ( self, cmd ):
        self.cmd = cmd

class illegalConfig ( Error ):
    """ Exception raised for using ppn > 16 on community nodes """

    def __init__ ( self, attr ):
        self.attr       =       attr
