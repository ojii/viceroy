import os

from flask import Flask
from slimit import ast

from .api import build_test_case
from .api import VICEROY_JS_PATH
from .contrib.flask import ViceroyFlaskTestCase
from .utils import extract
from .utils import slimit_node_to_str


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTS_FILE_PATH = os.path.join(ROOT_DIR, 'tests', 'viceroy.js')

with open(os.path.join(ROOT_DIR, 'static', 'viceroy.html')) as fobj:
    VICEROY_HTML = fobj.read()

with open(VICEROY_JS_PATH) as fobj:
    VICEROY_JS = fobj.read()

with open(TESTS_FILE_PATH) as fobj:
    TESTS = fobj.read()


test_app = Flask(__name__)


@test_app.route('/')
def index():
    return VICEROY_HTML


@test_app.route('/viceroy.js')
def viceroy():
    return VICEROY_JS


@test_app.route('/tests.js')
def tests():
    return TESTS


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
         'VICEROY.exception', 'VICEROY.expected_failure', 'VICEROY.skip'],
        lambda node: slimit_node_to_str(node.args[0]),
        extractor=_extractor
    )

ViceroyTests = build_test_case(
    'ViceroyTests', TESTS_FILE_PATH, _viceroy, DummyTests
)


# class QunitTests(QUnitTestCase):
#     @unittest.expectedFailure
#     def test_fail(self):
#         self.assertInBrowser("""
#         test( "hello fail", function() {
#           deepEqual( 1 , "1", "Failed!" );
#         });
#         """)
#
#     def test_success(self):
#         self.assertInBrowser("""
#         test( "hello success", function() {
#           equal( 1 , "1", "Success!" );
#         });
#         """)
#
#
# class JasmineTests(JasmineTestCase):
#     suite_name = "A suite"
#
#     def test_spec_success(self):
#         self.assertInBrowser("""
#         it("contains spec with an expectation", function() {
#             expect(true).toBe(true);
#         });
#         """)
#
#     @unittest.expectedFailure
#     def test_spec_fail(self):
#         self.assertInBrowser("""
#         it("contains spec with an failing expectation", function() {
#             expect(true).toBe(false);
#         });
#         """)
