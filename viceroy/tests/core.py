import os
import unittest

from slimit import ast
from flask import Flask

from viceroy.api import build_test_case
from viceroy.api import JavascriptError
from viceroy.constants import VICEROY_ROOT
from viceroy.constants import VICEROY_JS_PATH
from viceroy.contrib.flask import ViceroyFlaskTestCase
from viceroy.utils import extract
from viceroy.utils import slimit_node_to_str


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SUCCESS_TESTS_FILE_PATH = os.path.join(
    ROOT_DIR, 'js', 'viceroy', 'success.js'
)
FAIL_TESTS_FILE_PATH = os.path.join(
    ROOT_DIR, 'js', 'viceroy', 'fail.js'
)

with open(os.path.join(VICEROY_ROOT, 'static', 'viceroy.html')) as fobj:
    VICEROY_HTML = fobj.read()

with open(VICEROY_JS_PATH) as fobj:
    VICEROY_JS = fobj.read()

with open(SUCCESS_TESTS_FILE_PATH) as fobj:
    SUCCESS_TESTS = fobj.read()

with open(FAIL_TESTS_FILE_PATH) as fobj:
    FAIL_TESTS = fobj.read()


test_app = Flask(__name__)
fail_app = Flask(__name__)


@test_app.route('/')
@fail_app.route('/')
def index():
    return VICEROY_HTML


@test_app.route('/viceroy.js')
@fail_app.route('/viceroy.js')
def viceroy():
    return VICEROY_JS


@test_app.route('/tests.js')
def success():
    return SUCCESS_TESTS


@fail_app.route('/tests.js')
def fail():
    return FAIL_TESTS


class BaseTestCase(ViceroyFlaskTestCase):
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
    'ViceroySuccessTests', SUCCESS_TESTS_FILE_PATH, _viceroy, BaseTestCase
)


class ViceroyFailureTests(build_test_case('Base', FAIL_TESTS_FILE_PATH,
                                          _viceroy, BaseTestCase)):
    viceroy_flask_app = fail_app

    @unittest.expectedFailure
    def test_test_fail(self):
        super().test_test_fail()

    def test_test_error(self):
        self.assertRaises(JavascriptError, super().test_test_error)
