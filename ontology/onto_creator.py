import os
import sys
import javalang
import owlready2

from definitions import ROOT_DIR


def create_ontology():
    print('\n> Creating new ontology...')
    


def create_ontology_argparse(args):

    if args.source is None or not (os.path.exists(args.source) and os.path.isfile(args.source)):
        print('Enter a valid path to a a file "tree.py"...')
        sys.exit(0)

    create_ontology()
