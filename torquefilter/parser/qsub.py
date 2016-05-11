
import argparse

def qsub():
    """Initialize a parser for qsub style PBS directives"""


    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-a', dest='date_time', nargs=1, type=int)
    parser.add_argument('-A', dest='account_string', nargs=1)
    parser.add_arguemnt('-b', dest='seconds', nargs=1)
    parser.add_argument('-c', dest='checkpoint_options', nargs=1)
    parser.add_argument('-C', dest='directive_prefix', nargs=1)
    parser.add_argument('-d', dest='work_directory', nargs=1)
    parser.add_argument('-D', dest='root_directory', nargs=1)
    parser.add_argument('-e', dest='error_path', nargs=1)
    parser.add_argument('-f', dest='fault_tolerant', action='store_true')
    parser.add_argument('-h', dest='user_hold', action='store_true')
    parser.add_argument('-I', dest='interactive', action='store_true')
    parser.add_argument('-j', dest='join', nargs=1)
    parser.add_argument('-k', dest='keep', nargs=1)
    parser.add_argument('-l', dest='resource_list', nargs=1)
    parser.add_argument('-m', dest='mail_options', nargs=1)
    parser.add_argument('-M', dest='user_list', nargs=1)
    parser.add_argument('-N', dest='name', nargs=1)
    parser.add_argument('-o', dest='output_path', nargs=1)
    parser.add_argument('-p', dest='proxy_user', nargs=1)
    parser.add_argument('-q', dest='destination', nargs=1)
    parser.add_argument('-r', dest='rerunable', nargs=1)
    parser.add_argument('-S', dest='path_list', nargs=1)
    parser.add_argument('-t', dest='array_reqeust', nargs=1)
    parser.add_argument('-T', dest='script_name', nargs=1)
    parser.add_argument('-u', dest='user_list', nargs=1)
    parser.add_argument('-v', dest='variable_list', nargs=1)
    parser.add_argument('-V', dest='env_variables', action='store_true')
    parser.add_argument('-W', dest='additional_attributes', nargs=1)
    parser.add_argument('-x', dest='non_parse', action='store_true')
    parser.add_argument('-X', dest='Xforwarding', action='store_true')
    parser.add_argument('-z', dest='no_jobidentifier', action='store_true')

    return parser
