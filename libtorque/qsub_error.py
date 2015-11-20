#! /bin/env python
# User-defined Exceptions for libtorque python library

import sys

class Error ( Exception ):
    """ Base class for exceptions in libtorque module. """
    pass

class illegalMemReq ( Error ):
    """ Exception raised for illegal memory attributes within PBS. """

    def exit_message ( self ):
        sys.stderr.write ( "\n\tERROR: This system uses 'pvmem'" )
        sys.stderr.write ( "resource setting by default.\n" )
        sys.stderr.write ( "\tUsing 'vmem' and/or 'mem' resource on this" )
        sys.stderr.write ( " queue is not permitted.\n" )
        sys.stderr.write ( "\tSetting 'vmem' or 'mem' will not" )
        sys.stderr.write ( "change the default 'pvmem' " )
        sys.stderr.write ( "\n\tmemory setting of 3 GB which is the amount of " ) 
        sys.stderr.write ( "memory per process.\n\tPlease visit ")
        sys.stderr.write ( "http://goo.gl/vF3UgX for more information.\n\n\n" )

class illegalMemAttributes ( Error ):
    """ Exception raised for setting memory attributes greater than memory
    resources. """

    def __init__ ( self, totalMem, queue, pvmem, availMem ): 
        self.totalMem   =       str ( totalMem )
        self.queue      =       queue
        self.pvmem      =       str ( pvmem )
        self.availMem   =       str ( availMem )
        
    def exit_message ( self ):
        sys.stderr.write ( "\n\tERROR: You are requesting a total of " + \
                self.totalMem + " GB of memory per node.\n" )
        sys.stderr.write ( "\tMax memory per node is 54 GB in the " + \
                self.queue +  " queue. \n" )
        sys.stderr.write ( "\tBased on your current pvmem value of " + \
                self.pvmem + ", the max number for ppn can be " +  \
                self.availMem + ".\n" )
        sys.stderr.write ( "\tPlease visit http://goo.gl/vF3UgX for more" )
        sys.stderr.write ( "information.\n\n\n" )

class illegalCommand ( Error ):
    """ Exception raised for using illegal commands. """

    def __init__ ( self, cmd ):
        self.cmd = cmd

    def exit_message ( self ):
        sys.stderr.write ("\n\tERROR: Command '" + self.cmd +  \
            "' is not permitted to be executed on compute nodes.\n")
        sys.stderr.write ("\tPlease remove the use of '" + self.cmd + \
            "' from your submit script.\n")
        sys.stderr.write ("\tIf you feel this is in error, " + \
            "please open a help desk ticket at\n")
        sys.stderr.write ("\thttps://helpdesk.hpc.wvu.edu.\n\n\n")
