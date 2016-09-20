
from torquefilter.exceptions.error import illegalConfig
from torquefilter.exceptions.error import illegalMemConfig
from torquefilter.exceptions.error import illegalCommand

class subfilter:
    """
    Class that checks for illegal memory, illegal commands, and/or illegal 
    attributes in current PBSjob.  

    *queues*        -   A list of queues and their associated configurations (see queue class).
    *maps*          -   A class that has attributes *commands* and *attributes* for current job.
    *commands*      -   A list of illegal commands.
    *attributes*    -  A list of illegal qsub attributes.
    """

    def __init__(self, queueList=None, values=None, commands=None, attributes=None):

        # If no map supplied, return
        if (values):
            self.commands       =   values.commands
            self.attr           =   values.attributes
        else:
            return

        self.queueList  =   queueList
        self.illcomm    =   commands
        self.illattr    =   attributes

        if (commands):
            self.chk_commands()

        if (attributes):
            self.chk_attr()

        if (queueList):
            self.chk_memory()

    def chk_memory(self):
        """Check PBS resources for correct memory amount"""

        maxMem = 0

        # Return if community node not specified
        if 'queue' in self.attr:
            for queue in self.queueList:
                if self.attr['queue'] is queue.name:
                    checkMem = True
                    maxMem = queue.memLimit
        else:
            return True

        if (not checkMem):
            return True

        # Define processor per node
        if 'procs' in self.attr:
            if (int(self.attr['procs']) > 16):
                ppn = 16
            else:
                ppn = int(self.attr['procs'])
        elif 'ppn' in self.attr:
            ppn = int(self.attr['ppn'])
        else:
            ppn = 1

        if (ppn > 16):
            raise illegalConfig(self.attr)

        # Return if memory not specified 
        if 'pvmem' not in self.attr:
            return True

        pvmem_orig = self.attr['pvmem']
        pvmem = self.attr['pvmem'].lower ()
       
        if pvmem.endswith("gb") or pvmem.endswith("gw"):
            power = 0   
        elif pvmem.endswith("mb") or pvmem.endswith("mw"):
            power = 1
        elif pvmem.endswith("kb") or pvmem.endswith("kw"):
            power = 2
        elif pvmem.endswith("b") or pvmem.endswith("w"):
            power = 3
        else:
            return False

        pvmem = pvmem.strip("gmkbw")
        pvmem = float(pvmem) / 1024 ** power
        totalMem = pvmem * ppn
        availMem = maxMem / pvmem

        if (totalMem > maxMem):
            raise illegalMemConfig (int(totalMem), self.attr['queue'], \
                                pvmem_orig, int(availMem ))

        return True

        
    def chk_attr (self):

        # Exit for illegal memory management attributes
        for attr in self.illattr:
            if (attr in self.attr):
                raise illegalConfig(attr)

    def chk_commands(self):
        
        for cmd in self.commands:
            if cmd[0] in self.illcomm:
                raise illegalCommand(cmd[0])

