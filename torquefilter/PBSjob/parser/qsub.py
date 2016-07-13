
from torquefilter.exceptions.parser import ArgumentParserError

import argparse

class ModifiedArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		raise ArgumentParserError(message)

def qsub():
    """Initialize a parser for qsub style PBS directives"""

    parser = ModifiedArgumentParser('qsubParser', add_help=False)

    # Add arguments
    parser.add_argument('-a', dest='date_time', nargs=1, type=int, 
            default=argparse.SUPPRESS)
    parser.add_argument('-A', dest='account_string', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-b', dest='seconds', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-c', dest='checkpoint_options', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-C', dest='directive_prefix', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-d', dest='work_directory', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-D', dest='root_directory', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-e', dest='error_path', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-f', dest='fault_tolerant', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('-h', dest='user_hold', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('-I', dest='interactive', action='store_true', 
            default=False)
    parser.add_argument('-j', dest='join', nargs=1, default=argparse.SUPPRESS)
    parser.add_argument('-k', dest='keep', nargs=1, default=argparse.SUPPRESS)
    parser.add_argument('-l', dest='resource_list', nargs=1, action='append', 
            default=argparse.SUPPRESS)
    parser.add_argument('-m', dest='mail_options', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-M', dest='user_list', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-N', dest='name', nargs=1, default=argparse.SUPPRESS)
    parser.add_argument('-o', dest='output_path', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-p', dest='proxy_user', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-q', dest='destination', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-r', dest='rerunable', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-S', dest='path_list', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-t', dest='array_reqeust', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-T', dest='script_name', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-u', dest='user_list', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-v', dest='variable_list', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-V', dest='env_variables', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('-W', dest='additional_attributes', nargs=1, 
            default=argparse.SUPPRESS)
    parser.add_argument('-x', dest='non_parse', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('-X', dest='Xforwarding', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('-z', dest='no_jobidentifier', action='store_true', 
            default=argparse.SUPPRESS)
    parser.add_argument('remain', nargs=argparse.REMAINDER)

    return parser

def parseUsage(self):
    """ Print qsub usage message if argparse Error occurs """

    sys.stderr.write ( "usage: qsub [-a data_time] [-A account_string] [-" )
    sys.stderr.write ( "b secs]\n\t[-c [ none | { enabled | periodic | " )
    sys.stderr.write ( "shutdown |\n\tdepth=<int> | dir=<path> | interva " )
    sys.stderr.write ( "l=<minutes>}... ]\n\t[-C directive_prefix] -d pa" )
    sys.stderr.write ( "th] [-D path]\n\t[-e path] [-h] [-I] [-j oe|eo|n]" )
    sys.stderr.write ( " [-k {oe}] [-l resource_list] [-m n|{abe}]\n\t" )
    sys.stderr.write ( "[-M user_list] [-N jobname] [-o path] [-p " )
    sys.stderr.write ( "priority] [-P proxy_user [-J <jobid]]\n\t" )
    sys.stderr.write ( "[-q queue] [-r y|n] [-S path] [-t number_to_" )
    sys.stderr.write ( "submit] [-T type] [-u user_list] [-w] path\n\t" )
    sys.stderr.write ( "[-W additional_attributes] [-v variable_list]" )
    sys.stderr.write ( " [-V] [-x] [-X] [-z] [script]\n\n" )

    return
