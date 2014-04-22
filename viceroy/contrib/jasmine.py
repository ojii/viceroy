from viceroy.utils import extract
from viceroy.utils import slimit_node_to_str


def jasmine(source):
    yield from extract(
        source,
        ['it'],
        lambda node: slimit_node_to_str(node.args[0])
    )

