import os
import sys
import owlready2

from definitions import ONTO_PATH


def populate_ontology(onto, source):
    print(onto, source)


def populate_ontology_argparse(args):
    if args.source is None or not os.path.exists(args.source):
        print('Enter a valid path to a directory containing java files...')
        sys.exit(0)
    elif not (os.path.exists(ONTO_PATH) and os.path.isfile(ONTO_PATH)):
        print('Ontology "%s" does not exist ...' % os.path.basename(ONTO_PATH))
        sys.exit(0)

    onto = owlready2.get_ontology(ONTO_PATH).load()

    populate_ontology(onto=onto, source=args.source)
