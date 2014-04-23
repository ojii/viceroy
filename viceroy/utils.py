from slimit.parser import Parser
from slimit.ast import FunctionCall
from slimit.ast import Identifier


def _recurse(node, test_method_names, get_name, extractor):
    test_name = extractor(node)
    if test_name and test_name in test_method_names:
        yield get_name(node)
    for child in node.children():
        if child is None:
            continue
        if isinstance(child, list):
            continue
        yield from _recurse(child, test_method_names, get_name, extractor)


def _extractor(node):
    if isinstance(node, FunctionCall):
        if isinstance(node.identifier, Identifier):
            return node.identifier.value
    return None


def extract(source, test_method_names, get_name, extractor=_extractor):
    tree = Parser().parse(source)
    yield from _recurse(tree, test_method_names, get_name, extractor)


def slimit_node_to_str(node):
    s = node.to_ecma()
    if s[0] == s[-1] and s[0] in ["'", '"']:
        return s[1:-1]
    else:
        return s
