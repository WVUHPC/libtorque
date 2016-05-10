
import argparse

def qsub():
    "Initialize a parser for qsub style PBS directives"

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_arguments('-N', dest='name', nargs=1)

    return parser
