
Auditing
========

The jobauditer class provides the ability to record information about submitted
jobs.  You can record the values of PBS attributes. Or record the percentage of
jobs that use a specific command.  Additionally, you can record specific values
of certain arguments for commands.  For instance::

    from torquefilter import audit

    tellme = audit.jobauditer(current_job)
    tellme.init()

    tellme.commandArgs('mpirun', ['-np'])

    tellme.runaudit()

will capture the value of the '-np' argument of all mpirun commands; allowing
you to capture the size range of parallel jobs.


JSON Output
===========

The output of runaudit() is a JSON file.  The location of the JSON file is
controlled by the init() method.  Each job audited will create a single JSON
file output.
