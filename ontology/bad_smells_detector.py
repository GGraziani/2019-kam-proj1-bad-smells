import os
import sys
from owlready2 import get_ontology, default_world
import rdflib
import rdflib.plugins.sparql as sq

from definitions import P_ONTO_PATH, QUERIES_PATH


def find_bad_smells():

    print('\n> Running queries for detecting bad smells in "%s"... ' % os.path.basename(P_ONTO_PATH))

    if not os.path.exists(QUERIES_PATH):
        os.makedirs(QUERIES_PATH)

    graph = default_world.as_rdflib_graph()

    get_long_methods_and_constructors(g=graph)
    get_large_classes(g=graph)
    get_methods_or_constructors_with_switch(g=graph)
    get_methods_or_constructors_with_long_parameter_list(g=graph)
    get_data_classes(g=graph)


def exec_query(query, g):
    q = sq.prepareQuery(
        query,
        initNs={"tree": "http://my.onto.org/tree.owl#"}
    )
    return g.query(q)


def get_long_methods_and_constructors(g):

    print('\t - Searching for "LongMethod, LongConstructor"...', end='')

    methods = exec_query(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 20)
        """, g)

    out = open(QUERIES_PATH+"/1. LongMethod-LongConstructor.txt", "w")
    out.write("1.1 - Long Method:\n\n")
    for row in methods:
        out.write(row.cn+" : "+row.mn+" - "+row.tot+" statements\n")

    constructors = exec_query(
        """SELECT ?cn ?con ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?cd .
                ?cd a tree:ConstructorDeclaration .
                ?cd tree:jname ?con .
                ?cd tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?cd
            HAVING (COUNT(?s) >= 20)
        """, g)

    out.write("\n\n1.2 - Long Constructor:\n\n")
    for row in constructors:
        out.write(row.cn+" : "+row.con+" : "+row.tot+" statements\n")

    out.close()

    print(' saved in "1. LongMethod-LongConstructor.txt"')


def get_large_classes(g):

    print('\t - Searching for "Large Class"...', end='')

    classes = exec_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?cn
            HAVING (COUNT(?m) >= 10)
        """, g)

    out = open(QUERIES_PATH+"/2. LargeClass.txt", "w")
    out.write("2 - Large Class:\n\n")
    for row in classes:
        out.write(row.cn+" : "+row.tot+" methods\n")

    out.close()

    print(' saved in "2. LargeClass.txt"')


def get_methods_or_constructors_with_switch(g):

    print('\t - Searching for "MethodWithSwitch, ConstructorWithSwitch"...', end='')

    methods = exec_query(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a tree:SwitchStatement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 1)
        """, g)

    out = open(QUERIES_PATH+"/3. MethodWithSwitch-ConstructorWithSwitch.txt", "w")
    out.write("3.1 - Method With Switch:\n\n")
    for row in methods:
        out.write(row.cn+" : "+row.mn+"\n")

    constructors = exec_query(
        """SELECT ?cn ?con ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?o .
                ?cd a tree:ConstructorDeclaration .
                ?cd tree:jname ?con .
                ?cd tree:body ?s .
                ?s a tree:SwitchStatement .
            } GROUP BY ?cd
        """, g)

    out.write("\n\n3.2 - Long Constructor:\n\n")
    for row in constructors:
        out.write(row.cn+" : "+row.con+"\n")

    out.close()

    print(' saved in "3. MethodWithSwitch-ConstructorWithSwitch.txt"')


def get_methods_or_constructors_with_long_parameter_list(g):

    print('\t - Searching for "MethodWithLongParameterList, ConstructorWithLongParameterList"...', end='')

    methods = exec_query(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:parameters ?s .
                ?s a tree:FormalParameter .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 5)
        """, g)

    out = open(QUERIES_PATH+"/4. MethodWithLongParameterList-ConstructorWithLongParameterList.txt", "w")
    out.write("4.1 - Method With Long Parameter List:\n\n")
    for row in methods:
        out.write(row.cn+" : "+row.mn+" - "+row.tot+" parameters\n")

    constructors = exec_query(
        """SELECT ?cn ?con ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?cd .
                ?cd a tree:ConstructorDeclaration .
                ?cd tree:jname ?con .
                ?cd tree:parameters ?s .
                ?s a tree:FormalParameter .
            } GROUP BY ?cd
            HAVING (COUNT(?s) >= 5)
        """, g)

    out.write("\n\n4.2 - Constructor With Long Parameter List:\n\n")
    for row in constructors:
        out.write(row.cn+" : "+row.con+" : "+row.tot+" parameters\n")

    out.close()

    print(' saved in "4. MethodWithLongParameterList-ConstructorWithLongParameterList.txt"')


def get_data_classes(g):

    print('\t - Searching for "DataClass"...', end='')

    getters_setters = exec_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                FILTER (regex(?mn, "get.*") || regex(?mn, "set.*"))
            } GROUP BY ?cn
        """, g)

    out = open(QUERIES_PATH+"/5. DataClass.txt", "w")
    out.write("5 - Data Class:\n\n")

    all_methods = exec_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?cn
        """, g)

    for row in getters_setters:
        tot = get_class(row.cn, all_methods)
        is_data_class = str(row.tot == tot.tot)
        out.write('%s : %s filtered - %s unfiltered => DataClass: %s\n' % (row.cn, row.tot, tot.tot, is_data_class))

    out.close()

    print(' saved in "5. DataClass.txt"')


def get_class(name, class_list):
    for el in class_list:
        if el.cn == name:
            return el
    return None


def find_bad_smells_argparse(args):
    if not (os.path.exists(P_ONTO_PATH) and os.path.isfile(P_ONTO_PATH)):
        print('Ontology "%s" does not exist ...' % os.path.basename(P_ONTO_PATH))
        sys.exit(0)

    get_ontology(P_ONTO_PATH).load()

    find_bad_smells()
