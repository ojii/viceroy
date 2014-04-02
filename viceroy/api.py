import inspect
import abc
import os
import unittest
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from viceroy.utils import build_test_cases
from viceroy.utils import build_timeout_test_case
from viceroy.utils import ComparisonResult
from viceroy.utils import Result


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASEDIR, 'static')


class Viceroy(object):
    viceroy_path = os.path.join(STATIC, 'viceroy.js')

    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout

    def _js(self, script):
        return self.browser.execute_script(script)

    def load(self, src):
        with open(src) as fobj:
            self._js(fobj.read())

    def run(self, scripts):
        self.load(self.viceroy_path)
        for script in scripts:
            self.load(script)
        self._wait('return Viceroy.is_done();')
        return self._js('return Viceroy.get_results();')

    def _wait(self, until):
        WebDriverWait(self.browser, self.timeout).until(
            lambda _: self._js(until)
        )


class BaseTestCase(unittest.TestCase):
    pass


class BaseTestSuite(unittest.TestSuite, metaclass=abc.ABCMeta):
    test_file_path = abc.abstractproperty()
    setup_script = None
    runner_script = None
    scripts = []

    driver_class = webdriver.WebDriver
    viceroy_class = Viceroy
    index_url = '/static/index.html'
    timeout = 100

    def __init__(self):
        self._test_cases = None
        self.root = os.path.dirname(self.test_file_path)
        self.filename = os.path.basename(self.test_file_path)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __iter__(self):
        if self._test_cases is None:
            self._test_cases = self._build()
        for test_case in self._test_cases:
            yield test_case

    def _build(self):
        if not self.test_file_path:
            return []
        browser = self.driver_class()
        try:
            viceroy = self.viceroy_class(browser, self.timeout)
            scripts = []
            scripts.extend(self.scripts)
            if self.setup_script is not None:
                scripts.append(self.setup_script)
            scripts.append(self.test_file_path)
            if self.runner_script is not None:
                scripts.append(self.runner_script)
            test_results = viceroy.run(scripts)
            results = self.get_results(test_results)
            return build_test_cases(self.__class__.__name__, results)
        except TimeoutException as exc:
            return build_timeout_test_case(self.__class__.__name__, exc)
        finally:
            browser.quit()

    def get_results(self):
        raise NotImplementedError()


class BaseQunitTestSuite(BaseTestSuite, metaclass=abc.ABCMeta):
    scripts = [
        os.path.join(BASEDIR, 'static/qunit/qunit.js'),
    ]
    setup_script = os.path.join(BASEDIR, 'static/qunit/setup.js')
    runner_script = os.path.join(BASEDIR, 'static/qunit/runner.js')

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


class BaseJasminTestSuite(BaseTestSuite, metaclass=abc.ABCMeta):
    scripts = [
        os.path.join(BASEDIR, 'static/jasmine/jasmine.js'),
        os.path.join(BASEDIR, 'static/jasmine/jasmine-html.js'),
        os.path.join(BASEDIR, 'static/jasmine/boot.js'),
    ]
    setup_script = os.path.join(BASEDIR, 'static/jasmine/setup.js')
    runner_script = os.path.join(BASEDIR, 'static/jasmine/runner.js')

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
