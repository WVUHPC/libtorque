#!/bin/env python

import torquefilter

torquefilter.ill_comm ( ['qsub', 'msub', 'ssh', 'scp'] )
torquefilter.queues ( ['comm_mmem_week', 'comm_mmem_day'] )

torquefilter.runfilter ()

