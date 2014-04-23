from viceroy.scanner import BaseScanner


class JasmineScanner(BaseScanner):
    def visit_FunctionCall_xdescribe(self, node):
        raise StopIteration()

    def visit_FunctionCall_it(self, node):
        yield self.extract_name(node.args[0])
