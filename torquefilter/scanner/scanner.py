
import sys
import re

class scanner:
    "Run file scanner"

    def __init__(self, mapper, parser):
        self.mapper = mapper
        self.parser = parser

    def parse_command(self, line):
        """Strip lines designated as commands of file descriptors and/or shell
        piping characters"""

        processed_commands = []

        # Split line into terminated statements, then by pipe
        for statement in line.split(';'):
            for part in statement.split('|'):
                # Remove patterns - <file.txt <<file.txt from start of command
                new = re.sub(r'^< ?[\w\.]*', '', part)
                new = re.sub(r'^>{1,2} ?[\w\.]*', '', new)
                # Remove pipeing commands from the end of the command
                new = re.sub(r'< ?[\w\.]*$', '', new)
                new = re.sub(r'>{1,2} ?[\w\.]*$', '', new)

                # Append command to list
                processed_commands.append(new.strip(' '))
        
        # Return all Commands
        return processed_commands

    def runparser(self, fn, printfile=True, outfile=False):
        """Scan qsub file (or STDIN) identifing PBS directives or commands and
        process according."""


        if ('STDIN' == fn):
            infd = sys.stdin
        else:
            infd = open(fn, 'r')

        args = []
        parse_directives = True

        # Setup outfile if any
        if (outfile):
            output = open(outfile, 'w')
        else:
            output = sys.stdout

        for line in infd:
            # Make sure submit script echoed to STDOUT for qsub command
            if (printfile):
                output.write(line)
            # Skip empty lines or lines with only whitespace
            if (re.match (r'^\s*$', line)):
                continue;

            line = line.strip('\n')
            if (line.startswith('#')):
                if (line.startswith('#PBS ')):
                    if (parse_directives):
                        for directive in line.lstrip('#PBS ').split( ' ' ):
                            # join strings, not append; nested lists will fail 
                            # argparse()
                            args += directive
            else:
                if (parse_directives):
                    # future directives will not be parsed
                    parse_directives = False
                for cmd in self.parse_command(line):
                    self.mapper.add_command(cmd)

        # Parse Options only if there are arguments
        if (args):
            attributes = vars(self.parser.parse_args(args))
            self.mapper.add_attribute(attributes)
        

        if (outfile):
            output.close()
        infd.close()
               
