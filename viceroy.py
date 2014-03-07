import abc
from collections import namedtuple
from contextlib import contextmanager
import inspect
import multiprocessing
import os
import unittest

from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.wait import WebDriverWait

try:
    from http import server
except ImportError:
    import SimpleHTTPServer as server


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASEDIR, 'static')

API = '''
window.PJTVS_DONE = false;
window.PJTVS_RESULTS = [];

window.pjtvs_done = function(results){
    window.PJTVS_RESULTS = results;
    window.PJTVS_DONE = true;
};
'''


Result = namedtuple('Result', 'name passed message')
ComparisonResult = namedtuple('Result', 'name passed message expected actual')


class BaseHandler(server.SimpleHTTPRequestHandler):
    test_file = None
    static_root = None
    favicon = (
        b'AAABAAEAEBACAAEAAQCwAAAAFgAAACgAAAAQAAAAIAAAAAEAAQAAAAAAgAAAAAAAAAAA'
        b'AAAAAAAAAAAAAAAAAAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//wAA//8AAP//AAD//wAA//8A'
        b'AP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA'
    )
    favicon_size = len(favicon)

    def do_GET(self):
        """Serve a GET request."""
        if self.path == '/favicon.ico':
            self.send_favicon()
        elif self.path == '/tests.js':
            self.send_tests()
        elif self.path.startswith('/static/'):
            self.send_static()
        else:
            self.send_error(404, 'File not found')

    def _send_file(self, path):
        content_type = self.guess_type(path)
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", os.stat(path).st_size)
        self.end_headers()
        with open(path, 'rb') as fobj:
            self.copyfile(fobj, self.wfile)

    def send_favicon(self):
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        self.send_header("Content-Length", self.favicon_size)
        self.end_headers()
        self.wfile.write(self.favicon)

    def send_tests(self):
        self._send_file(self.test_file)

    def send_static(self):
        path = os.path.join(self.static_root, self.path[8:])
        if os.path.exists(path):
            self._send_file(path)
        else:
            self.send_error(404, "File not found")

    def log_date_time_string(self):
        pass

    def log_error(self, format, *args):
        pass

    def log_message(self, format, *args):
        pass

    def log_request(self, code='-', size='-'):
        pass


def _server(static_root, test_file, port, event):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the first command line
    argument).

    """
    handler = type('Handler', (BaseHandler, ), {
        'static_root': static_root,
        'test_file': test_file,
    })

    httpd = server.HTTPServer(('localhost', 0), handler)

    port.value = httpd.socket.getsockname()[1]
    event.set()
    httpd.serve_forever()


@contextmanager
def run_server(static_root, test_file):
    port = multiprocessing.Value('i', 0)
    event = multiprocessing.Event()

    proc = multiprocessing.Process(
        target=_server,
        args=(static_root, test_file, port, event)
    )
    proc.start()
    event.wait()
    yield port.value
    proc.terminate()


def wait_for_js_to_stop(browser, timeout=10):
    WebDriverWait(browser, timeout).until(
        lambda _: browser.execute_script('return window.PJTVS_DONE;')
    )


def wait_for_dom_ready(browser, timeout=10):
    WebDriverWait(browser, timeout).until(
        lambda _: browser.execute_script(
            'return document.readyState;'
        ) == 'complete'
    )


class BaseTestCase(unittest.TestCase):
    pass


def test_method_factory(result):
    def test_method(self):
        if not result.passed:
            if isinstance(result, ComparisonResult):
                self.assertEqual(
                    result.actual,
                    result.expected,
                    result.message
                )
            else:
                self.fail(result.message)
    test_method.__doc__ = result.name
    return test_method


def build_test_cases(name, results):
    attrs = {}
    for i, result in enumerate(results):
        attrs['test_method'.format(i)] = test_method_factory(result)
        yield type(name, (unittest.TestCase,), attrs)('test_method')


class BaseTestSuite(unittest.TestSuite, metaclass=abc.ABCMeta):
    test_file_path = abc.abstractproperty() 

    driver_class = webdriver.WebDriver
    index_url = None
    timeout = 10

    def __init__(self):
        self._test_cases = None
        self.root = os.path.dirname(self.test_file_path)
        self.filename = os.path.basename(self.test_file_path)

    def _build(self):
        if not self.test_file_path:
            return []
        with run_server(STATIC, self.test_file_path) as port:
            browser = self.driver_class()
            try:
                url = 'http://localhost:{}{}'.format(port, self.index_url)
                browser.get(url)
                wait_for_dom_ready(browser, self.timeout)
                browser.execute_script(API)
                browser.execute_script('window.pjtvs_start();')
                wait_for_js_to_stop(browser, self.timeout)
                tests = browser.execute_script('return window.PJTVS_RESULTS;')
                results = self.get_results(tests)
                return build_test_cases(self.__class__.__name__, results)
            finally:
                browser.quit()

    def __iter__(self):
        if self._test_cases is None:
            self._test_cases = self._build()
        for test_case in self._test_cases:
            yield test_case

    def get_results(self):
        raise NotImplementedError()


class BaseQunitTestSuite(BaseTestSuite, metaclass=abc.ABCMeta):
    index_url = '/static/qunit/index.html'

    def get_results(self, results):
        for result in results:
            if 'expected' in result:
                yield ComparisonResult(
                    result['name'],
                    result['result'],
                    result['message'],
                    result['expected'],
                    result['actual'],
                )
            else:
                yield Result(
                    result['name'],
                    result['result'],
                    result['message'],
                )


class BaseJasminTestSuite(BaseQunitTestSuite, metaclass=abc.ABCMeta):
    index_url = '/static/jasmine/index.html'

    timeout = 10

    def get_results(self, results):
        for result in results:
            yield ComparisonResult(
                result['name'],
                result['passed'],
                result['message'],
                result['expected'],
                result['actual'],
            )


def auto_load_tests(attrs):
    def load_tests(loader, tests, pattern):
        suite = unittest.TestSuite()
        for obj in attrs.values():
            if (isinstance(obj, type) and
                    not inspect.isabstract(obj) and
                    issubclass(obj, BaseTestSuite)):
                suite.addTest(obj())
        return suite
    return load_tests
