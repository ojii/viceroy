import os
import unittest

from flask import Flask

from viceroy.api import build_test_case
from viceroy.api import JavascriptError
from viceroy.constants import VICEROY_JS_PATH
from viceroy.contrib.flask import ViceroyFlaskTestCase
from viceroy.scanner import BaseScanner


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SUCCESS_TESTS_FILE_PATH = os.path.join(
    ROOT_DIR, 'js', 'viceroy', 'success.js'
)
FAIL_TESTS_FILE_PATH = os.path.join(
    ROOT_DIR, 'js', 'viceroy', 'fail.js'
)

with open(os.path.join(ROOT_DIR, 'js', 'viceroy', 'viceroy.html')) as fobj:
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


class ViceroyScanner(BaseScanner):
    test_methods = {
        'VICEROY.store_result': 0,
        'VICEROY.success': 0,
        'VICEROY.fail': 0,
        'VICEROY.skip': 0,
        'VICEROY.start_test': 0,
    }


ViceroySuccessTests = build_test_case(
    'ViceroySuccessTests',
    SUCCESS_TESTS_FILE_PATH,
    ViceroyScanner,
    BaseTestCase
)


class ViceroyFailureTests(build_test_case('Base', FAIL_TESTS_FILE_PATH,
                                          ViceroyScanner, BaseTestCase)):
    viceroy_flask_app = fail_app

    @unittest.expectedFailure
    def test_test_fail(self):
        super().test_test_fail()

    def test_test_error(self):
        self.assertRaises(JavascriptError, super().test_test_error)


class TestScanner(unittest.TestCase):
    def test_simple(self):
        attrs = {
            'test_methods': {
                'test': 0
            }
        }
        cls = type('TestScanner', (BaseScanner, ), attrs)
        scanner = cls("test('foo')")
        names = list(scanner)
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'foo')

    def test_namespaced(self):
        attrs = {
            'test_methods': {
                'namespace.test': 0
            }
        }
        cls = type('TestScanner', (BaseScanner, ), attrs)
        scanner = cls("namespace.test('foo')")
        names = list(scanner)
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'foo')
