import os

from flask import Flask

from viceroy.api import VICEROY_ROOT
from viceroy.api import VICEROY_JS_PATH


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
