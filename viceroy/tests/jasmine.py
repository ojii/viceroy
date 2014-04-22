import os

from flask import Flask
from flask import send_from_directory
from flask import send_file

from viceroy.api import build_test_case
from viceroy.constants import VICEROY_ROOT
from viceroy.contrib.jasmine import jasmine
from viceroy.contrib.flask import ViceroyFlaskTestCase


JASMINE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'js', 'jasmine')
)


app = Flask(__name__)


@app.route('/')
def index():
    return send_file(os.path.join(JASMINE_DIR, 'specrunner.html'))


@app.route('/jasmine/<path:filename>')
def send_qunit(filename):
    return send_from_directory(JASMINE_DIR, filename)


@app.route('/<path:filename>')
def send_viceroy(filename):
    return send_from_directory(os.path.join(VICEROY_ROOT, 'static'), filename)


class JasmineBase(ViceroyFlaskTestCase):
    viceroy_flask_app = app

    @classmethod
    def _start_flask_server(cls):
        @cls.viceroy_flask_app.route('/spec.js')
        def spec():
            return send_file(cls.viceroy_source_file)
        super()._start_flask_server()


build_jasmine_test = lambda name: build_test_case(
    'JasmineBaseTest',
    os.path.join(JASMINE_DIR, 'spec', name),
    jasmine,
    JasmineBase,
)


JasmineAnySpecTests = build_jasmine_test('core/AnySpec.js')
