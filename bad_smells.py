import sys
import argparse

from definitions import ROOT_DIR
from utils.doc_utils import *
from utils.misc import listget


# add one gateway function for each functionality

def create_ontology_gateway(args):
    from ontology import onto_creator
    onto_creator.create_ontology_argparse(args)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# add subparser for onto_creator
p_create_ontology = subparsers.add_parser('onto_creator')
p_create_ontology.add_argument('-s', '--source', dest='source', default=ROOT_DIR+'/lib/tree.py')
p_create_ontology.set_defaults(func=create_ontology_gateway)


def main(argv):
    helpstrings = {'-h', '--help'}

    command = listget(argv, 0, '').lower()

    # The user did not enter a command, or the entered command is not recognized.
    if command not in MODULE_DOCSTRINGS:
        print(DOCSTRING)
        if command == '':
            print('You are seeing the default help text because you did not choose a command.')
        elif command not in helpstrings:
            print('You are seeing the default help text because "%s" was not recognized' % command)
        return 1

    # The user entered a command, but no further arguments, or just help.
    argument = listget(argv, 1, '').lower()
    if argument in helpstrings:
        print(MODULE_DOCSTRINGS[command])
        return 1

    args = parser.parse_args(argv)
    args.func(args)

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
