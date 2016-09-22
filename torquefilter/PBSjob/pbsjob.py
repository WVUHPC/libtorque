
from torquefilter.PBSjob.mapper.pbsattr import PBSattr
from torquefilter.PBSjob.parser.qsub import qsub
from torquefilter.PBSjob.parser.qsub  import parseUsage
from torquefilter.scanner.scanner import scanner
from torquefilter.exceptions.parser import ArgumentParserError

import sys

class PBSjob():
    """
    torqueFilter class representing a PBS submission job.  These jobs use the 
    *qsub* command for job submission.  Additionally, they use the '#PBS' 
    directive for specifying job attributes.

    *PBSjob* class will parse command-line arguments and if specified, will read 
    and parse the batch job submit script.

    *args*  - Command-line arguments given to *qsub*, will default to sys.argv

    """

    def __init__(self, args=sys.argv):
        self.filename           =   None
        self.mapper             =   PBSattr()
        self.parser             =   qsub()
        self.scanner            =   scanner(self.mapper, self.parser)
        
        # Read CLI options for filename
        try:
            self.rtn_filename(args)
        except ArgumentParserError as err:
            print(err)
            parserUsage()
            sys.exit(2)

        if (not self.mapper.attributes['interactive']):
            try:
                self.scanner.runparser(self.filename)
            except IOError:
                sys.stderr.write("script file '" + self.filename + "' cannot be ")
                sys.stderr.write("loaded - No such file or directory\n\n")
                sys.exit(1)
            except ArgumentParserError as err:
                print(err)
                parserUsage()
                sys.exit(2)

    def rtn_filename(self, args):
        """ Given sys.argv[1:] return filename for input """

        attributes = vars(self.parser.parse_args(args[1:]))
        self.mapper.add_attribute(attributes)

        leftovers = attributes['remain']

        if (len(leftovers) == 1):
            self.filename = leftovers[0]
        elif (len(leftovers) > 1):
            sys.stderr.write("Index error\n\n")
            sys.exit(1)
        else:
            self.filename = "STDIN"

    def getCommands(self):
        """ Return commands list structure """

        return self.mapper.commands

    def getAttributes(self):
        """ Return PBS attributes dictionary """

        return self.mapper.attributes
