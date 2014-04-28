import os


VICEROY_ROOT = os.path.abspath(os.path.dirname(__file__))
VICEROY_STATIC_ROOT = os.path.join(VICEROY_ROOT, 'static')
VICEROY_JS_PATH = os.path.join(VICEROY_STATIC_ROOT, 'viceroy.js')
