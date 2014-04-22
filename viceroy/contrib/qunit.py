from viceroy.utils import extract
from viceroy.utils import slimit_node_to_str


def qunit(source):
    yield from extract(
        source,
        ['test', 'asyncTest'],
        lambda node: slimit_node_to_str(node.args[0]),
    )
