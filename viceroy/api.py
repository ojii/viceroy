import inspect
import abc
import os
import unittest

from selenium.webdriver.firefox import webdriver

from viceroy.selenium_utils import wait_for_dom_ready
from viceroy.selenium_utils import wait_for_js_to_stop
from viceroy.server import run_server
from viceroy.utils import build_test_cases
from viceroy.utils import ComparisonResult
from viceroy.utils import Result


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASEDIR, 'static')


VICEROY_SCRIPT = '''
window.VICEROY_DONE = false;
window.VICEROY_RESULTS = [];

window.viceroy_done = function(results){
    window.VICEROY_RESULTS = results;
    window.VICEROY_DONE = true;
};
'''


class BaseTestCase(unittest.TestCase):
    pass


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
                browser.execute_script(VICEROY_SCRIPT)
                browser.execute_script('window.viceroy_start();')
                wait_for_js_to_stop(browser, self.timeout)
                tests = browser.execute_script(
                    'return window.VICEROY_RESULTS;'
                )
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
    def load_tests(loader=None, tests=None, pattern=None):
        return auto_suite(attrs)
    return load_tests


def auto_suite(attrs):
    suite = unittest.TestSuite()
    for obj in attrs.values():
        if (isinstance(obj, type) and
                not inspect.isabstract(obj) and
                issubclass(obj, BaseTestSuite)):
            suite.addTest(obj())
    return suite
