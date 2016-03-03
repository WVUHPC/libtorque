.. torquefilter documentation master file, created by
   sphinx-quickstart on Mon Feb 29 16:10:53 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

torqueFilter Documentation
========================================

torqueFilter is a python module that makes creating efficient and powerful
PBS/torque submission filters effortlessly.  A complete submission filter can
be setup with as little as a few lines of code.  Additionally, torqueFilter
provides the ability to reject jobs by attribute configurations ( memory
request, CPU requests, etc... ), attribute types ( not supported attributes ),
and command types.  You can mix and match any number of filter rules to quickly
create powerful filters.

In addition to filter rules, torqueFilter provides the capability to audit
PBS settings and/or commands used in submitted jobs.  Audit functions allow
easy querying of how a distributed system is being utilized by it's users.  For
instance, you could quickly determine the number of processes requested for
each mpirun command, which modulefiles are being loaded, or how PBS attributes
are being used in combination.  

.. toctree::
   :maxdepth: 2

   start/index
   usage
   filter/index
   audit/index
