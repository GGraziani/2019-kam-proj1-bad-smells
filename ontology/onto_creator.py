import ast
import os
import sys
from owlready2 import get_ontology

from ontology.visitor import Visitor

from definitions import *

ONTO_PATH = os.path.join(RES_PATH, 'tree.owl')


def create_ontology(file_path):
    print('\n> Creating new ontology for file "%s"... ' % os.path.basename(file_path))

    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    onto = get_ontology("http://my.onto.org/tree.owl")

    visitor = Visitor(onto)
    visitor.visit(tree)
    onto.save(ONTO_PATH, format="rdfxml")

    print('> New ontology saved to file "%s"' % os.path.relpath(ONTO_PATH, ROOT_DIR))


def create_ontology_argparse(args):
    if args.source is None or not (os.path.exists(args.source) and os.path.isfile(args.source)):
        print('Enter a valid path to a a file "tree.py"...')
        sys.exit(0)

    create_ontology(file_path=args.source)
