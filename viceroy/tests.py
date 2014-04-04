import os

from viceroy.api import BASEDIR
from viceroy.api import BaseJasminTestSuite
from viceroy.api import BaseQunitTestSuite
from viceroy.api import auto_load_tests
from viceroy.api import auto_suite


class QunitTests(BaseQunitTestSuite):
    test_file_path = os.path.join(BASEDIR, 'js_tests', 'qunit.js')
    expected_failures = ["hello fail"]


class JasmineTests(BaseJasminTestSuite):
    test_file_path = os.path.join(BASEDIR, 'js_tests', 'jasmine.js')
    expected_failures = ["contains spec with an failing expectation"]


load_tests = auto_load_tests(locals())

suite = auto_suite(locals())
