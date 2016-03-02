
Simple Example
==============

Below is a straightforward example to see how the torqueFilter module is used
to build easy torque submission filters.  The python script below will reject
jobs that use the commands 'ssh' or 'qsub', as well as the PBS attribute 'mem'.
Additionally, the 'community' queue class will be checked for memory and CPU
configurations.::

    #!/bin/python

    import torquefilter

    illegalCommands = ['ssh', 'sub']
    illegalAttributes = ['mem']

    current_job = torquefilter.torqueFilter ()

    current_job.illComm ( illegalCommands )
    current_job.illAttr ( illegalAttributes )

    current_job.checkQueue ( ['community'] )

    current_job.runfilter ()


As you can see from this script.  There are two stages of a submission filter.
Set your illegal commands and attributes and/or specify which queue classes you
want checked.  Once you tell torqueFiler what you want checked for, you end the
submission script with the runfiler () method to execute the torqueFilter.
This script would be placed in /usr/local/sbin/torque_submitfilter so it is
executed by torque against all job submissions.
