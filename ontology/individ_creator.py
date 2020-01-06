import os
import sys
import javalang.tree
import owlready2

from definitions import *


def populate_ontology(onto, source):
    for file in os.listdir(source):
        if file.endswith('.java'):
            f_path = os.path.join(source, file)
            with open(f_path) as j_file:
                ast = javalang.parse.parse(j_file.read())
                process_file(ast, onto)

    # onto.save(P_ONTO_PATH, format="rdfxml")


def process_file(ast, onto):
    for _, node in ast.filter(javalang.tree.ClassDeclaration):
        cd = onto['ClassDeclaration']()
        cd.jname = [node.name]


def populate_ontology_argparse(args):
    if args.source is None or not os.path.exists(args.source):
        print('Enter a valid path to a directory containing java files...')
        sys.exit(0)
    elif not (os.path.exists(ONTO_PATH) and os.path.isfile(ONTO_PATH)):
        print('Ontology "%s" does not exist ...' % os.path.basename(ONTO_PATH))
        sys.exit(0)

    onto = owlready2.get_ontology(ONTO_PATH).load()

    populate_ontology(onto=onto, source=args.source)
