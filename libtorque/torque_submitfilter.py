#!/bin/env python
# torque_submitfilter
# Spruce Head Node srih0001

import sys, tempfile

import pbsattr
from qsubfile import qsubfile 

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
    maxMem = 54

    # Exit for illegal memory management attributes
    if ('vmem' in attr or 'mem' in attr):
        print >> sys.stderr,"\n\tERROR: This system uses 'pvmem' resource setting by default."
        print >> sys.stderr,"\tUsing 'vmem' and/or 'mem' resouce on this queue is not permitted."
        print >> sys.stderr,"\tSetting 'vmem' or 'mem' will not change the default 'pvmem' "
        print >> sys.stderr,"\tmemory setting of 3 GB, which is the amount of memory per process.\n"  
        print >> sys.stderr,"\tPlease visit http://goo.gl/vF3UgX for more information.\n"
        sys.exit(-1)

    # Return if memory not specified 
    if 'pvmem' not in attr:
        return

    pvmem = attr ['pvmem'].lower ()
    
    # Define processor per node
    if 'procs' in attr:
        if (int (attri ['procs']) > 16):
            ppn = 16
        else:
            ppn = int (attri ['procs'])
    elif 'ppn' in attr:
        ppn = int (attr ['ppn'])
    else:
        ppn = 1
       
    power = 0   
    # Get int value of pvmem
    if pvmem.endswith ("mb") or pvmem.endswith ("mw"):
        power = 1
    elif pvmem.endswith ("kb") or pvmem.endswith ("kw"):
        power = 2
    elif pvmem.endswith ("b") or pvmem.endswith ("w"):
        power = 3

    pvmem = pvmem.strip ("gmkbw")

    pvmem = float (pvmem) / 1024 ** power
    totalMem = pvmem * ppn
    availMem = maxMem / pvmem

    if (totalMem > maxMem):
        sys.stderr.write ("\n\tERROR: You are requesting a total of " + \
                str(totalMem) + " GB of memory per node.\n")
        sys.stderr.write ("\tMax memory per node is 54 GB in the " + \
                dictValues['queue'] +  " queue. \n")
        sys.stderr.write ("\tBased on your current pvmem value of " + \
                pvmemOrig + ", the max number for ppn can be " +  \
                str(int(availMem)) + ".\n")
        sys.stderr.write ("\tPlease visit http://goo.gl/vF3UgX for more information.\n")
        sys.exit(-1)

def chk_commands (commands):
    
    commandsToCheck = ["qsub", "msub", "ssh", "scp"]

    for cmd in commands:
        if cmd [0] in commandsToCheck:
            sys.stderr.write ("\n\tERROR: Command '" + cmd [0] +  \
                "' is not permitted to be executed on compute nodes.\n")
            sys.stderr.write ("\tPlease remove the use of '" + cmd [0] + \
                "' from your submit script.\n")
            sys.stderr.write ("\tIf you feel this is in error, " + \
                "please open a help desk ticket at\n")
            sys.stderr.write ("\thttps://helpdesk.hpc.wvu.edu.\n\n")
            sys.exit(-1)

def capture_modload (commands):

    # Open a temporary file to write to with a unique name
    tmpfile = tempfile.NamedTemporaryFile (dir = "./tmpJvyZn4", mode = 'w', \
                                        delete = False)

    # Write modulefiles loaded to tmpfile
    for cmd in commands:
        if 'module' in cmd [0]:
            if 'load' in cmd[1]:
                for module in cmd [2:]:
                    tmpfile.write (module)
                    tmpfile.write ("\n")

    tmpfile.close ()



def main ():
    """Interface CLI options and Qsubfile options given by qsub command"""

    # Create an empty job process
    curr_job = qsubfile ()

    filename = rtn_filename (curr_job) 
    
    # Add file directives and commands to PBS attributes
    if (curr_job.attr ['Interactive']):
        chk_memory (curr_job.attr)
    else:
        curr_job.processfile (filename)

        chk_memory (curr_job.attr)
        chk_commands (curr_job.comm)

        # If runnable - capture module command loads
        capture_modload (curr_job.comm)
    
    
    sys.exit(0)
    

if __name__ == '__main__':
    main()
