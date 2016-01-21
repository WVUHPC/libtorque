
import sys, tempfile
import os, stat, getopt

from qsub.qsubfile import qsubfile
from error.error import illegalMemReq, illegalMemAttributes, illegalCommand
from error.error import illegalConfig

def rtn_filename ( curr_obj ):
    """Given sys.argv[1:] return input of filename"""

    args = sys.argv [ 1: ]
    nargs = len ( args )

    if ( nargs >= 1 ):
        leftovers = curr_obj.commline ( args )

        if ( len ( leftovers ) == 1 ):
            filename = leftovers [ 0 ]
        elif ( len ( leftovers ) > 1 ):
            sys.stderr.write ( "Index error\n\n" )
            sys.exit ( 1 )
        else:
            filename = "STDIN"
    else:
        filename = "STDIN"

    return filename

def chk_memory ( attr ):
    """Check PBS resources for correct memory amount"""

    global __systemspecs__
    system = __systemspecs__

    # Return if community node not specified
    if 'queue' in attr:
        if attr ['queue'] not in system.queuesToCheck:
            return True
    else:
        return True


    # Define processor per node
    if 'procs' in attr:
        if (int (attr ['procs']) > 16):
            ppn = 16
        else:
            ppn = int (attr ['procs'])
    elif 'ppn' in attr:
        ppn = int (attr ['ppn'])
    else:
        ppn = 1

    if ( ppn > 16 ):
        raise illegalConfig ( attr ['queue'], attr ['ppn'] )

    # Exit for illegal memory management attributes
    if ('vmem' in attr or 'mem' in attr):
        raise illegalMemReq ()

    # Return if memory not specified 
    if 'pvmem' not in attr:
        return True

    pvmem_orig = attr ['pvmem']
    pvmem = attr ['pvmem'].lower ()
   
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
    availMem = maxMem / pvmem

    if (totalMem > system.maxMem):
        raise illegalMemAttributes ( int ( totalMem ), attr ['queue'], \
                            pvmem_orig, int ( availMem ) )

    return True

def chk_commands ( commands ):
    
    global __systemspecs__
    system = __systemspecs__
    
    for cmd in commands:
        if cmd [0] in system.commandsToCheck:
            raise illegalCommand ( cmd [0] )

def capture_modload ( commands ):

    # Open a temporary file to write to with a unique name
    tmpfile = tempfile.NamedTemporaryFile (dir = "/shared/moduleaudit", mode = 'w', \
                                        delete = False)

    filename = tmpfile.name
    # Write modulefiles loaded to tmpfile
    for cmd in commands:
        if 'module' in cmd [0]:
            if 'load' in cmd[1]:
                for module in cmd [2:]:
                    tmpfile.write (module)
                    tmpfile.write ("\n")

    tmpfile.close ()
    # Change permissions
    os.chmod ( filename, stat.S_IRUSR | stat.S_IWUSR \
            | stat.S_IROTH | stat.S_IWOTH ) 



def runfilter ():
    """ Run configured job submission filter """

    global __systemspecs__

    curr_job = qsubfile.qsubfile ()

    # Read CLI options for filename
    try:
        filename = rtn_filename ( curr_job )
    except getopt.GetoptError as err:
        print ( err )
        curr_job.usage ()
        sys.exit ( 2 )

    # Add file directives and commands to PBS attributes
    # if job is not interactive
    if ( not curr_job.attr ['Interactive'] ):
        try:
            curr_job.processfile ( filename )
        except IOError:
            sys.stderr.write ( "script file '" + filename + "' cannot be " )
            sys.stderr.write ( "loaded - No such file or directory\n\n" )
            sys.exit ( 1 )
        except getopt.GetoptError:
            print ( err )
            curr_job.usage ()
            sys.exit ( 2 )

    # Check for illegal commands
    if ( __systemspecs__.ill_comm ): 
        try:
            chk_commands ( curr_job.comm )
        except illegalCommand as e:
            e.exit_message ()
            sys.exit ( 1 )
        except:
            sys.exit ( 0 )

    # Check for illegal attributes
    if ( __systemspecs.ill_attr ):
        try:
            chk_rtn = chk_memory ( curr_job.attr )
        except illegalMemReq as e:
            e.exit_message ()
            sys.exit ( 1 )
        except illegalMemAttributes as e:
            e.exit_message ()
            sys.exit ( 1 )
        except illegalConfig as e:
            e.exit_message ()
            sys.exit ( 1 )
        except:
            sys.exit ( 0 )

    if ( not chk_rtn ):
        sys.exit ( 0 )

    # Audit module files
    if ( not curr_job.attr ['Interactive'] ):
        try:
            capture_modload ( curr_job.comm )
        except:
            sys.exit ( 0 )

    # Exit clean
    sys.exit ( 0 )
