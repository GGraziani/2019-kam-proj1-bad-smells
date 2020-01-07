import os
import sys
from owlready2 import get_ontology

from definitions import P_ONTO_PATH


def find_bad_smells(onto):
    print(onto)


def find_bad_smells_argparse(args):
    if not (os.path.exists(P_ONTO_PATH) and os.path.isfile(P_ONTO_PATH)):
        print('Ontology "%s" does not exist ...' % os.path.basename(P_ONTO_PATH))
        sys.exit(0)

    onto = get_ontology(P_ONTO_PATH).load()

    find_bad_smells(onto=onto)
