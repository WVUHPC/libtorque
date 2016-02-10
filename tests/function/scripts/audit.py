#!/bin/env python

import sys, os

# Set sys.path
cwd = os.getcwd ()
sys.path.append ( cwd )

# Now import module
import torquefilter
from torquefilter import audit

current_job = torquefilter.torqueFilter ()

# Run filter
current_job.runfilter ()


tellme = audit.jobauditer ()
tellme.init ( current_job )

tellme.command ( 'mpirun' )
tellme.command ( 'module', ['load'], 'Module Loads' )
tellme.commandArgs ( 'mpirun', ['-np', '-host'] )
tellme.commandSlice ( 'module', ['load'], start=2, tableName="Loaded Modules" )

tellme.attr ('queue')

tellme.runaudit ()
