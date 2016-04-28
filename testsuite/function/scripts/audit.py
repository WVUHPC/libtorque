#!/bin/env python

import sys, os

# Set sys.path
cwd = os.getcwd ()
sys.path.append ( cwd )

# Now import module
import torquefilter
from torquefilter import audit

# Remove tmp filename from command-line parameters
outputfile = sys.argv.pop ()

current_job = torquefilter.torqueFilter ()

# Run filter
current_job.runfilter ()

tellme = audit.jobauditer ( current_job )
tellme.init ( outputfile )

tellme.command ( 'mpirun' )
tellme.command ( 'module', ['load'] )
tellme.commandArgs ( 'mpirun', ['-np', '-host'] )
tellme.commandSlice ( 'module', ['load'], start=2, tableName="Loaded Modules" )

tellme.attr ('queue')

tellme.runaudit ()

