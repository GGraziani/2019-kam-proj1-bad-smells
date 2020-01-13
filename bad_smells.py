import sys
import argparse

from definitions import *
from utils.doc_utils import *
from utils.misc import listget, mkdir


# add one gateway function for each functionality

def create_ontology_gateway(args):
    from ontology import onto_creator
    onto_creator.create_ontology_argparse(args)


def populate_ontology_gateway(args):
    from ontology import individ_creator
    individ_creator.populate_ontology_argparse(args)


def bad_smells_gateway(args):
    from ontology import bad_smells_detector
    bad_smells_detector.find_bad_smells_argparse(args)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# add subparser for onto_creator
p_create_ontology = subparsers.add_parser('onto_creator')
p_create_ontology.add_argument('-p', '--path', dest='path', default=TREE_PATH)
p_create_ontology.set_defaults(func=create_ontology_gateway)

# add subparser for individ_creator
p_populate_ontology = subparsers.add_parser('individ_creator')
p_populate_ontology.add_argument('-s', '--source', dest='source', default=SOURCE_PATH)
p_populate_ontology.set_defaults(func=populate_ontology_gateway)

# add subparser for bad_smells_detector
p_bad_smells = subparsers.add_parser('find_bad_smells')
p_bad_smells.set_defaults(func=bad_smells_gateway)


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

    mkdir(os.path.join(PROJ_ROOT, 'res'))

    args = parser.parse_args(argv)
    args.func(args)

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
