
from mapper.pbsattr import PBSattr
from parser.parser import qsub
from parser.parser import parserUsage

class PBSjob(PBSattr):

    def __init__(self, args):
        self.filename           =   None
        self.mapper             =   PBSattr()
        self.parser             =   qsub()
        
        # Read CLI options for filename
        try:
            self.rtn_filename()
        except ArgumentParserError as err:
            print(err)
            parserUsage()
            sys.exit(2)

    def rtn_filename(self):
        """ Given sys.argv[1:] return filename for input """

        args = sys.argv[1:]
        nargs = len(args)

        if (nargs >= 1):
            attributes = vars(self.parser.parse_args(args))

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
