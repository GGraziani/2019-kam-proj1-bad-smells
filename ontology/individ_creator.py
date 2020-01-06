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

    onto.save(P_ONTO_PATH, format="rdfxml")


def process_file(ast, onto):
    for _, node in ast.filter(javalang.tree.ClassDeclaration):
        cd = onto['ClassDeclaration']()
        cd.jname = [node.name]
        for member in node.body:
            create_member(cd, member, onto)


def create_member(cd, member, onto):
    if type(member) == javalang.tree.FieldDeclaration:
        create_fields(cd, member, onto)
    elif type(member) == javalang.tree.MethodDeclaration or type(member) == javalang.tree.ConstructorDeclaration:
        create_method(cd, member, onto)


def create_fields(cd, field, onto):
    for f in field.declarators:
        fd = onto['FieldDeclaration']()
        fd.jname = [f.name]
        cd.body.append(fd)


def create_method(cd, method, onto):
    md = onto[method.__class__.__name__]()
    md.jname = [method.name]
    add_stmts(md, method, onto)
    add_params(md, method, onto)
    cd.body.append(md)


def add_stmts(md, method, onto):
    for _, statement in method.filter(javalang.tree.Statement):
        if type(statement) != javalang.tree.Statement:
            s_type = statement.__class__.__name__
            s = onto[s_type]()
            md.body.append(s)


def add_params(md, method, onto):
    for _, statement in method.parameters:
        fp = onto['FormalParameter']()
        md.parameters.append(fp)


def populate_ontology_argparse(args):
    if args.source is None or not os.path.exists(args.source):
        print('Enter a valid path to a directory containing java files...')
        sys.exit(0)
    elif not (os.path.exists(ONTO_PATH) and os.path.isfile(ONTO_PATH)):
        print('Ontology "%s" does not exist ...' % os.path.basename(ONTO_PATH))
        sys.exit(0)

    onto = owlready2.get_ontology(ONTO_PATH).load()

    populate_ontology(onto=onto, source=args.source)
