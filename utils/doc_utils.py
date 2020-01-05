from utils.misc import indent

DOCSTRING = '''
Knowledge Analysis and Management 2019 - Bad Smells
by Gustavo Graziani

Commands:
{onto_creator}


TO SEE DETAILS ON EACH COMMAND, RUN
> python3 bad_smells.py <command>
'''

MODULE_DOCSTRINGS = {
    'onto_creator': '''
onto_creator:
     Creates an ontology for Java entities.

    Example usage:
        $ python3 bad_smells.py onto_creator

    flags:
    -s <path-to-file> | --source <path-to-path>:
        The path to the "tree.py" file. Default is "ROOT_DIR/lib/tree.py"
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
