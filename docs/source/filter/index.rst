

Filter Rules
==============

All filtering related functions occur with the high level torqueFilter class.
Essentially, however, when the runfilter() method is executed, torqueFilter
will parse the commandline arguments that where passed to qsub and additionally
parse the submitted file.  Commands and PBS attributes are recorded, and the
submitted file is printed out to stdout (for correct torque functioning
post-processing).  Whether the submitted file is then accepted by torque or not
is based on the exit status of torqueFilter.  If the submission file violates
any of the rules set by you before runfilter() executes, the job is rejected.


.. toctree::
    :maxdepth: 1

    class
    error


