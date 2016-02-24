#!/bin/env python

import sys, os

# Set sys.path
cwd = os.getcwd ()
sys.path.append ( cwd )

# Now import module
import torquefilter
from torquefilter import error

current_job = torquefilter.torqueFilter ()

current_job.illComm ( ['qsub', 'msub', 'ssh', 'scp'] )
current_job.checkQueue ( ['comm_mmem_week', 'comm_mmem_day'] )
current_job.illAttr ( ['vmem', 'mem'] )

# Run filter

try:
    current_job.runfilter ()

except error.illegalCommand as e:
    sys.stderr.write ("\n\tERROR: Command '" + e.cmd +  \
        "' is not permitted to be executed on compute nodes.\n")
    sys.stderr.write ("\tPlease remove the use of '" + e.cmd + \
        "' from your submit script.\n")
    sys.stderr.write ("\tIf you feel this is in error, " + \
        "please open a help desk ticket at\n")
    sys.stderr.write ("\thttps://helpdesk.hpc.wvu.edu.\n\n\n")
    sys.exit ( 1 )
    
except error.illegalMemReq:
    sys.stderr.write ( "\n\tERROR: This system uses 'pvmem'" )
    sys.stderr.write ( "resource setting by default.\n" )
    sys.stderr.write ( "\tUsing 'vmem' and/or 'mem' resource on this" )
    sys.stderr.write ( " queue is not permitted.\n" )
    sys.stderr.write ( "\tSetting 'vmem' or 'mem' will not" )
    sys.stderr.write ( " change the default 'pvmem' " )
    sys.stderr.write ( "\n\tmemory setting of 3 GB which is the amount of " ) 
    sys.stderr.write ( "memory per process.\n\tPlease visit ")
    sys.stderr.write ( "http://goo.gl/vF3UgX for more information.\n\n\n" )
    sys.exit ( 1 )
    
except error.illegalMemConfig as e:
    sys.stderr.write ( "\n\tERROR: You are requesting a total of " + \
            e.totalMem + " GB of memory per node.\n" )
    sys.stderr.write ( "\tMax memory per node is 54 GB in the " + \
            e.queue +  " queue. \n" )
    sys.stderr.write ( "\tBased on your current pvmem value of " + \
            e.pvmem + ", the max number for ppn can be " +  \
            e.availMem + ".\n" )
    sys.stderr.write ( "\tPlease visit http://goo.gl/vF3UgX for more" )
    sys.stderr.write ( " information.\n\n\n" )
    sys.exit ( 1 )

except error.illegalConfig as e:
    sys.stderr.write ( "\n\tERROR: You are requesting " + e.attr['ppn'] + \
        " processors per node in the " + e.attr['queue'] + "\n\tqueue class." )
    sys.stderr.write ( " You can only request a maximum of 16 cores " + \
        "in " + e.attr['queue'] + ".\n" )
    sys.stderr.write ( "\tThis can be done by reducing your ppn setting to " + \
        "below 16.\n\n\n")
    sys.exit ( 1 ) 
except Exception:
    sys.exit ( 0 )

sys.exit ( 0 )


