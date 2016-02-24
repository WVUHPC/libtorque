
import sys, tempfile
import os, stat, getopt

from torquefilter.error import illegalConfig, illegalCommand
from torquefilter.error import illegalMemReq, illegalMemConfig
from torquefilter.qsub import qsubfile

class torqueFilter ( qsubfile.qsubfile ):
    """ User class for job submissions """

    def __init__ ( self ):
        self.queuesToCheck          =   []
        self.commandsToCheck        =   []
        self.attrToCheck            =   []
        self.maxMem                 =   54
        self.attr                   =   {}
        self.comm                   =   []
        self.attr ['Interactive']   =   False

    def checkQueue ( self, queues ):
        """ Add list of queues to queuesToCheck """

        for name in queues:
            self.queuesToCheck.append ( name )

    def illComm ( self, commands ):
        """ Add list of commands to commandsToCheck """

        for cmd in commands:
            self.commandsToCheck.append ( cmd );

    def illAttr ( self, attr ):
        """ Add illegal attributes to attrToCheck """

        for name in attr:
            self.attrToCheck.append ( name )


    def rtn_filename ( self ):
        """ Given sys.argv[1:] set filename for input """

        args = sys.argv [ 1: ]
        nargs = len ( args )

        if ( nargs >= 1 ):
            leftovers = self.commline ( args )

            if ( len ( leftovers ) == 1 ):
                self.filename = leftovers [ 0 ]
            elif ( len ( leftovers ) > 1 ):
                sys.stderr.write ( "Index error\n\n" )
                sys.exit ( 1 )
            else:
                self.filename = "STDIN"
        else:
            self.filename = "STDIN"

    def chk_memory ( self ):
        """Check PBS resources for correct memory amount"""

        # Return if community node not specified
        if 'queue' in self.attr:
            if self.attr ['queue'] not in self.queuesToCheck:
                return True
        else:
            return True


        # Define processor per node
        if 'procs' in self.attr:
            if (int (self.attr ['procs']) > 16):
                ppn = 16
            else:
                ppn = int (self.attr ['procs'])
        elif 'ppn' in self.attr:
            ppn = int (self.attr ['ppn'])
        else:
            ppn = 1

        if ( ppn > 16 ):
            raise illegalConfig ( self.attr )

        # Return if memory not specified 
        if 'pvmem' not in self.attr:
            return True

        pvmem_orig = self.attr ['pvmem']
        pvmem = self.attr ['pvmem'].lower ()
       
        if pvmem.endswith ( "gb" ) or pvmem.endswith ( "gw" ):
            power = 0   
        elif pvmem.endswith ( "mb" ) or pvmem.endswith ( "mw" ):
            power = 1
        elif pvmem.endswith ( "kb" ) or pvmem.endswith ( "kw" ):
            power = 2
        elif pvmem.endswith ( "b" ) or pvmem.endswith ( "w" ):
            power = 3
        else:
            return False

        pvmem = pvmem.strip ("gmkbw")
        pvmem = float ( pvmem ) / 1024 ** power
        totalMem = pvmem * ppn
        availMem = self.maxMem / pvmem

        if (totalMem > self.maxMem):
            raise illegalMemConfig ( int ( totalMem ), self.attr ['queue'], \
                                pvmem_orig, int ( availMem ) )

        return True

        
    def chk_attr ( self ):

        # Exit for illegal memory management attributes
        for attr in self.attrToCheck:
            if ( attr in self.attr):
                raise illegalMemReq ()

    def chk_commands ( self ):
        
        for cmd in self.comm:
            if cmd [0] in self.commandsToCheck:
                raise illegalCommand ( cmd [0] )


    def runfilter ( self ):
        """ Run configured job submission filter """

        # Read CLI options for filename
        try:
            self.rtn_filename ()
        except getopt.GetoptError as err:
            print ( err )
            self.usage ()
            sys.exit ( 2 )

        # Add file directives and commands to PBS attributes
        # if job is not interactive
        if ( not self.attr ['Interactive'] ):
            try:
                self.processfile ( self.filename )
            except IOError:
                sys.stderr.write ( "script file '" + self.filename + "' cannot be " )
                sys.stderr.write ( "loaded - No such file or directory\n\n" )
                sys.exit ( 1 )
            except getopt.GetoptError:
                print ( err )
                self.usage ()
                sys.exit ( 2 )
    
            # Check for illegal commands
            self.chk_commands ()

        # Check illegal attributes on all jobs ( including interactive )
        self.chk_attr ()

        chk_rtn = self.chk_memory ()
