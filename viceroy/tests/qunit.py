import os

from flask import Flask
from flask import send_from_directory

from viceroy.api import build_test_case
from viceroy.constants import VICEROY_ROOT
from viceroy.contrib.qunit import qunit
from viceroy.contrib.flask import ViceroyFlaskTestCase


QUNIT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'js', 'qunit')
)


app = Flask(__name__)

@app.route('/qunit/<path:filename>')
def send_qunit(filename):
    return send_from_directory(QUNIT_DIR, filename)

@app.route('/<path:filename>')
def send_viceroy(filename):
    return send_from_directory(os.path.join(VICEROY_ROOT, 'static'), filename)


class QUnitBase(ViceroyFlaskTestCase):
    viceroy_flask_app = app


QUnitBaseTests = build_test_case(
    'QUnitBaseTests',
    os.path.join(QUNIT_DIR, 'test.js'),
    qunit,
    QUnitBase,
    viceroy_url='/qunit/test.html'
)
