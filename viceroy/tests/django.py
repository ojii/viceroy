import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'viceroy.tests.djangoapp.settings'

from viceroy.api import build_test_case
from viceroy.contrib.django import ViceroyDjangoTestCase
from .core import ViceroyScanner

root = os.path.abspath(os.path.dirname(__file__))
test_file = os.path.join(root, 'djangoapp', 'static', 'tests.js')

ViceroyDjangoTests = build_test_case(
    'ViceroyDjangoTests',
    test_file,
    ViceroyScanner,
    ViceroyDjangoTestCase,
)
