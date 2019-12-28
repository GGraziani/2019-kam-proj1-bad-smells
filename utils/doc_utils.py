from utils.misc import indent

DOCSTRING = '''
2019-proj1-bad-smells
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
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
