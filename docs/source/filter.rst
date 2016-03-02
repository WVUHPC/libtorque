
torqueFilter class
==================

All filtering related functions occur with the high level torqueFilter class.
Essentially, however, when the runfilter() method is executed, torqueFilter
will parse the commandline arguments that where passed to qsub and additionally
parse the submitted file.  Commands and PBS attributes are recorded, and the
submitted file is printed out to stdout (for correct torque functioning
post-processing).  Whether the submitted file is then accepted by torque or not
is based on the exit status of torqueFilter.  If the submission file violates
any of the rules set by you before runfilter() executes, the job is rejected.


Custom Error Handling
=====================

Most systems are going to want to supply custom error messages when certain
rules are violated.  For instance, informing the user why there jobs have been
rejected.  torqueFilter will raise unique exceptions for different rules
violations, allowing you to catch the exceptions and write custom error
messages.  A simple example::

    try:
        current_job.runfilter()
    except error.illegalCommand as e:
        sys.stderr.write( "ERROR: Command '" + e.cmd + "' is not allowed.\n")
        sys.exit(1)

The above will output "...Command is not allowed" with the specific command
that violates the illComm rules as e.cmd.  There are unique exceptions for
different rules, and each provide captured job attributes so error messages can
even include job specific information to the user.
