import unittest

from slimit import ast

from viceroy.api import build_test_case
from viceroy.api import JavascriptError
from viceroy.contrib.flask import ViceroyFlaskTestCase
from viceroy.utils import extract
from viceroy.utils import slimit_node_to_str

from .utils import test_app
from .utils import fail_app
from .utils import SUCCESS_TESTS_FILE_PATH
from .utils import FAIL_TESTS_FILE_PATH


class DummyTests(ViceroyFlaskTestCase):
    viceroy_flask_app = test_app


def _extractor(node):
    if not isinstance(node, ast.FunctionCall):
        return None
    if not isinstance(node.identifier, ast.DotAccessor):
        return None
    if not isinstance(node.identifier.identifier, ast.Identifier):
        return None
    if not isinstance(node.identifier.node, ast.Identifier):
        return None
    return '{}.{}'.format(
        node.identifier.node.value, node.identifier.identifier.value
    )


def _viceroy(source):
    yield from extract(
        source,
        ['VICEROY.store_result', 'VICEROY.success', 'VICEROY.fail',
         'VICEROY.exception', 'VICEROY.expected_failure', 'VICEROY.skip',
         'VICEROY.start_test'],
        lambda node: slimit_node_to_str(node.args[0]),
        extractor=_extractor
    )

ViceroySuccessTests = build_test_case(
    'ViceroySuccessTests', SUCCESS_TESTS_FILE_PATH, _viceroy, DummyTests
)


class ViceroyFailureTests(build_test_case('Base', FAIL_TESTS_FILE_PATH,
                                          _viceroy, DummyTests)):
    viceroy_flask_app = fail_app

    @unittest.expectedFailure
    def test_test_fail(self):
        super().test_test_fail()

    def test_test_error(self):
        self.assertRaises(JavascriptError, super().test_test_error)
