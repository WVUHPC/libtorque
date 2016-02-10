#!/bin/env python

import sys, os

# Set sys.path
cwd = os.getcwd ()
sys.path.append ( cwd )

# Now import module
import torquefilter

current_job = torquefilter.torqueFilter ()

current_job.illComm ( ['qsub', 'msub', 'ssh', 'scp'] )
current_job.checkQueue ( ['comm_mmem_week', 'comm_mmem_day'] )
current_job.illAttr ( ['vmem', 'mem'] )

# Run filter
current_job.runfilter ()

