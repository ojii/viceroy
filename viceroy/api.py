import contextlib
import warnings
import unittest

from .server import Server
from .server import QUnitServer
from .server import JasmineServer


class ViceroyTestCase(unittest.TestCase):
    server_class = Server
    url = '/'

    def get_driver(self):
        from selenium.webdriver.firefox import webdriver
        return webdriver.WebDriver()

    @contextlib.contextmanager
    def run_server(self, javascript):
        httpd = self.server_class(javascript)
        try:
            httpd.run_async()
            yield httpd
        finally:
            httpd.stop()

    def assertInBrowser(self, javascript):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            driver = self.get_driver()
            try:
                with self.run_server(javascript) as httpd:
                    driver.get('http://localhost:{}{}'.format(
                        httpd.port, self.url
                    ))
                    result = httpd.wait()
            finally:
                driver.quit()
            if result.failed:
                self.fail(result.error)


class QUnitTestCase(ViceroyTestCase):
    server_class = QUnitServer


class JasmineTestCase(ViceroyTestCase):
    server_class = JasmineServer
