import ast
from owlready2 import *


class Visitor(ast.NodeVisitor):

    def __init__(self, onto):
        self.onto = onto

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        with self.onto as onto:
            if type(node) == ast.ClassDef:
                for a in node.bases:
                    if a.id == "Node":
                        types.new_class(node.name, (Thing,))
                    else:
                        types.new_class(node.name, (onto[a.id],))

            elif type(node) == ast.Assign:
                for b in node.value.elts:
                    if b.s != "body" and b.s != "parameters" and b.s != "name":
                        types.new_class(b.s, (DataProperty,))
                    if b.s == "name":
                        types.new_class("jname", (DataProperty,))
                    if b.s == "body" or b.s == "parameters":
                        types.new_class(b.s, (ObjectProperty,))

