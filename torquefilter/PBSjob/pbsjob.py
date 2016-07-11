
from mapper.pbsattr import PBSattr
from parser.qsub import qsub
from parser.qsub  import parseUsage
from torquefilter.exceptions.parser import ArgumentParserError

import sys
from argparse import ArgumentParser

class PBSjob():

    def __init__(self, args=sys.argv[1:0]):
        self.filename           =   None
        self.mapper             =   PBSattr()
        self.parser             =   qsub()
        
        # Read CLI options for filename
        try:
            self.rtn_filename(args)
        except ArgumentParserError as err:
            print(err)
            parserUsage()
            sys.exit(2)

    def rtn_filename(self, args):
        """ Given sys.argv[1:] return filename for input """

        nargs = len(args)

        if (nargs >= 1):
            attributes = vars(self.parser.parse_args(args))
            self.mapper.add_attribute(attributes)

            if 'remain' in attributes:
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

