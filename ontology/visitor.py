import ast
from owlready2 import *


class Visitor(ast.NodeVisitor):

    def __init__(self, onto):
        self.onto = onto

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        with self.onto as onto:
            if type(node) == ast.ClassDef:
                for obj in node.bases:
                    if obj.id == "Node":
                        types.new_class(node.name, (Thing,))
                    else:
                        types.new_class(node.name, (onto[obj.id],))

            elif type(node) == ast.Assign:
                for el in node.value.elts:
                    if el.s == "body" or el.s == "parameters":
                        types.new_class(el.s, (ObjectProperty,))
                    elif el.s == "name":
                        types.new_class("jname", (DataProperty,))
                    elif el.s != "name":
                        types.new_class(el.s, (DataProperty,))
