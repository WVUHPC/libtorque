
from mapper.pbsattr import PBSattr
from parser.qsub import qsub
from parser.qsub  import parseUsage
from torquefilter.scanner.scanner import scanner
from torquefilter.exceptions.parser import ArgumentParserError

import sys

class PBSjob():

    def __init__(self, args):
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

        nargs = len(args[1:])
        if (nargs >= 1):
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
        else:
            self.filename = "STDIN"

