
Filter Error Handling
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
