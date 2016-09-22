#!/bin/env python

import sys, os

# Set sys.path
cwd = os.getcwd()
sys.path.append(cwd)

# Now import module
import torquefilter
from torquefilter import filter

illcommands = ['qsub', 'msub', 'ssh', 'scp']
illAttr = ['vmem', 'mem']

queueList = []
queueList.append(filter.queue("comm_mmem_week", 54))
queueList.append(filter.queue("comm_mmem_day", 54))

currentjob = torquefilter.PBSjob()

# Run Filter
try:
    filter.subfilter(queueList, currentjob, illcommands, illAttr)
except illegalCommand:
    sys.exit(1)
except illegalMemConfig:
    sys.exit(1)
except illegalConfig:
    sys.exit(1) 
except Exception:
    sys.exit(0)
sys.exit(0)
