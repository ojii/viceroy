from slimit.ast import Identifier
from slimit.parser import Parser


class BaseScanner(object):
    def __init__(self, source):
        self.tree = Parser().parse(source)
        self.x = 0

    def __iter__(self):
        for node in self.tree:
            yield from self.visit(node)

    def visit(self, node):
        method_name = 'visit_{}'.format(node.__class__.__name__)
        yield from getattr(self, method_name, self.generic_visit)(node)

    def visit_children(self, node):
        for child in node:
            yield from self.visit(child)

    def generic_visit(self, node):
        for child in node:
            yield from self.visit(child)

    def visit_FunctionCall(self, node):
        if isinstance(node.identifier, Identifier):
            function_name = node.identifier.value
            method_name = 'visit_FunctionCall_{}'.format(function_name)
            method = getattr(self, method_name, None)
            if method is not None:
                yield from method(node)
            else:
                yield from self.visit_children(node)
        else:
            yield from self.visit_children(node)

    def extract_name(self, node):
        s = node.to_ecma()
        if s[0] == s[-1] and s[0] in ["'", '"']:
            return s[1:-1]
        else:
            return s
