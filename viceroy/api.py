import contextlib
import unittest

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from .exceptions import ResultNotFound
from .exceptions import JavascriptError


class ViceroyTestCase(unittest.TestCase):
    viceroy_url = '/'
    viceroy_timeout = 30
    viceroy_driver_class = WebDriver

    @classmethod
    @contextlib.contextmanager
    def viceroy_server(cls):
        raise NotImplementedError()

    @classmethod
    @contextlib.contextmanager
    def viceroy_driver(cls):
        driver = None
        try:
            driver = cls.viceroy_driver_class()
            yield driver
        finally:
            if driver is not None:
                driver.quit()


    @classmethod
    def viceroy_get_results(cls):
        with cls.viceroy_server() as port:
            with cls.viceroy_driver() as driver:
                driver.get(
                    'http://localhost:{}{}'.format(port, cls.viceroy_url)
                )
                WebDriverWait(
                    driver,
                    cls.viceroy_timeout
                ).until(
                    lambda _: driver.execute_script(
                        'return window.VICEROY && window.VICEROY.DONE;'
                    )
                )
                return driver.execute_script('return window.VICEROY.RESULTS;')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.viceroy_cache = cls.viceroy_get_results()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'viceroy_cache'):
            del cls.viceroy_cache
        super().tearDownClass()


def test_method_proxy(full_name, short_name):
    def test_method(self):
        result = self.viceroy_cache.get(short_name, None)
        if result is None:
            result = self.viceroy_cache.get('viceroy_javascript_error', None)
            if result is None:
                keys = self.viceroy_cache.keys()
                raise ResultNotFound(
                    'Result for {!r} not found. Available results: {}'.format(
                        short_name, ', '.join(
                            '{!r}'.format(key) for key in keys
                        )
                    )
                )
        if result['code'] == '.':
            return
        elif result['code'] == 'F':
            self.fail(result['message'])
        elif result['code'] == 'E':
            raise JavascriptError(result['message'])
        elif result['code'] == 's':
            raise unittest.SkipTest(result['message'])
    test_method.__name__ = full_name
    return test_method


def build_test_case(class_name, source_file, scanner_class,
                    base_class, **extra_attrs):
    with open(source_file) as fobj:
        source = fobj.read()

    scanner = scanner_class(source)

    test_method_names = set(scanner)

    attrs = {'viceroy_source_file': source_file}
    for test_name in test_method_names:
        full_name = 'test_{}'.format(test_name)
        attrs[full_name] = test_method_proxy(full_name, test_name)

    attrs.update(extra_attrs)

    return type(class_name, (base_class,), attrs)
