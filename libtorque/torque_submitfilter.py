#!/bin/env python
# torque_submitfilter
# Spruce Head Node srih0001

import sys, tempfile
import os, stat

import pbsattr
from qsubfile import qsubfile 
from qsub_error import illegalMemReq, illegalMemAttributes, illegalCommand

def rtn_filename (curr_obj):
    """Given sys.argv[1:] return input of filename"""

    args = sys.argv[1:]
    nargs = len (args)

    if (nargs >= 1):
        leftovers = curr_obj.parseOpts (args)

        if (len (leftovers) > 0):
            filename = leftovers [0]
        else:
            filename = "STDIN"
    else:
        filename = "STDIN"

    return filename
  
def chk_memory (attr):
    """Check PBS resources for correct memory amount"""

    queuesToCheck = ['comm_mmem_week', 'comm_mmem_day']

    # Return if community node not specified
    if 'queue' in attr:
        if attr ['queue'] not in queuesToCheck:
            return True
    else:
        return True

    maxMem = 54

    # Exit for illegal memory management attributes
    if ('vmem' in attr or 'mem' in attr):
        raise illegalMemReq ()

    # Return if memory not specified 
    if 'pvmem' not in attr:
        return True

    pvmem_orig = attr ['pvmem']
    pvmem = attr ['pvmem'].lower ()
   
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

    if (totalMem > maxMem):
        raise illegalMemAttributes ( int ( totalMem ), attr ['queue'], \
                            pvmem_orig, int ( availMem ) )

    return True

def chk_commands (commands):
    
    commandsToCheck = ["qsub", "msub", "ssh", "scp"]

    for cmd in commands:
        if cmd [0] in commandsToCheck:
            raise illegalCommand ( cmd [0] )

def capture_modload (commands):

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


def main ():
    """Interface CLI options and Qsubfile options given by qsub command"""

    # Create an empty job process
    curr_job = qsubfile ()

    try:
        filename = rtn_filename ( curr_job ) 
    except getopt.GetoptError:
        sys.exit ( 0 )
    except:
        sys.exit ( 0 )
    
    # Add file directives and commands to PBS attributes
    # if job is not interactive
    if ( not curr_job.attr ['Interactive'] ):
        try:
            curr_job.processfile ( filename )
        except OSError:
            # Let qsub deal with I/O Errors as normal
            sys.exit ( 0 )
        except getopt.GetoptError:
            sys.exit ( 0 )
        except:
            sys.exit ( 0 )

        # Check commands and capture module files as well
        try:
            chk_commands ( curr_job.comm )
        except illegalCommand as e:
            e.exit_message ()
            sys.exit ( -1 )
        except:
            sys.exit ( 0 )

     
    # Check memory on all Jobs
    try:
        chk_rtn = chk_memory ( curr_job.attr )
    except illegalMemReq as e:
        e.exit_message ()
        sys.exit ( -1 )
    except illegalMemAttributes as e:
        e.exit_message ()
        sys.exit ( -1 )
    except:
        sys.exit ( 0 )

    # Illegal memory attributes - qsub will catch error
    if ( not chk_rtn ):
        sys.exit ( 0 )

    # Audit module files
    if ( not curr_job.attr ['Interactive'] ):
        capture_modload ( curr_job.comm )

    # Exit clean if everything appears correct
    sys.exit ( 0 )
    

if __name__ == '__main__':
    main()
