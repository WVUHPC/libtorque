import sys, re, getopt

from pbsattr import PBSattr

class qsubfile (PBSattr):
    "Class for PBS directives during job submission files"

    def parse_comm (self, line):
        """Strip lines designed as commands of file descriptors and/or shell
        piping characters"""

        processed_commands = []

        # Split line into terminated statements, then by pipe
        for statement in line.split (';'):
            for part in statement.split ('|'):
                # Remove patterns - <file.txt <<file.txt from start of command
                new = re.sub (r'^< ?[\w\.]*', '', part)
                new = re.sub (r'^>{1,2} ?[\w\.]*', '', new)
                # Remove pipeing commands from the end of the command
                new = re.sub (r'< ?[\w\.]*$', '', new)
                new = re.sub (r'>{1,2} ?[\w\.]*$', '', new)

                # Append command to list
                processed_commands.append (new.strip (' '))
        
        # Return all Commands
        return processed_commands

    def parseOpts (self, options):
        """Parse options list, sending each value to the correct PBSattr
        method"""

        # Map datatype to store locally (allowing for duplication)
        tmp_attr = { }

        opts, args = getopt.gnu_getopt (options, "q:l:I")
            
        for o, a in opts:
            if o in ("-q"):
                tmp_attr ['queue'] = a
            elif o in ("-l"):
                # Parse resource into mapping attribute
                for type in a.split (','):
                    for each in type.split (':'):
                        if ('=' in each):
                            keyword, value = each.split ('=')
                            tmp_attr [keyword] = value
                    else:
                        tmp_attr [each] = True
            elif o in ("-I"):
                tmp_attr ['Interactive'] = True
            else:
                continue

        # Now send mapping structure to PBS attr to add to global file class
        PBSattr.add_attr (self, tmp_attr)


    def processfile (self, fn):
        """Scan qsub file (or STDIN) identifing PBS directives or commands and
        process according."""

        input = open (fn, 'r')
        args = [ ]
        incommands = False

        for line in input:
            line = line.strip('\n')
            if (line.startswith ('#')):
                if (line.startswith ('#PBS ')):
                    if (not incommands):
                        for directive in line.strip ('#PBS ').split (' '):
                            args.append (directive)
                    else:
                        sys.stderr.write ("%s not processed" 
                                % line.strip ('#PBS'))
            else:
                if (not incommands):
                    incommands = True
                for each in self.parse_comm (line):
                    PBSattr.add_command (self, each)

        # Parse Options in correct order
        self.parseOpts (args)

               
