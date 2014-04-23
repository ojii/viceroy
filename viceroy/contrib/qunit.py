from viceroy.scanner import BaseScanner


class QUnitScanner(BaseScanner):
    def visit_FunctionCall_test(self, node):
        yield self.extract_name(node.args[0])

    def visit_FunctionCall_asyncTest(self, node):
        yield self.extract_name(node.args[0])
