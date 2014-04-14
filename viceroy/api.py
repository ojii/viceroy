import contextlib
import http
import json
import threading
import collections
import os
import unittest


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASEDIR, 'static')
Result = collections.namedtuple('Result', 'failed error')


def url(src):
    def decorator(meth):
        meth.viceroy_src = src
        return meth
    return decorator


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response, content_type = self.server_thread.urls.get(
            self.path, (None, None)
        )
        if response and content_type:
            status = 200
        else:
            response = b'Not found'
            content_type = 'text/plain'
            status = 404
        self._send(status, response, content_type)

    def do_POST(self):
        if self.path == '/viceroy-api/':
            raw_data = self.rfile.read()
            result = json.loads(raw_data.decode('utf8'))
            self.server_thread.notify(result)
        else:
            self._send(404, b'', 'text/plain')

    def _send(self, status, response, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)


class ServerThread(threading.Thread):
    def __init__(self, port_event, done_event, urls):
        self.port_event = port_event
        self.done_event = done_event
        self.port = None
        self.result = None
        self.server = None
        self.urls = urls
        super().__init__()

    def run(self):
        handler_class = type(
            'Handler',
            (RequestHandler,),
            {'server_thread': self}
        )
        self.server = http.server.HTTPServer(('localhost', 0), handler_class)
        self.port = self.server.server_port
        self.port_event.set()
        try:
            self.server.serve_forever()
        except Exception as exc:
            self.result = Result(True, 'VICEROY:INTERNAL:{}'.format(exc))
            self.done_event.set()

    def terminate(self):
        print('terminate')
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()

    def notify(self, result):
        self.result = Result(result['failed'], result['message'])
        print('notified')
        self.done_event.set()


class Server(object):
    def __init__(self, javascript):
        with open(os.path.join(STATIC, 'viceroy.js'), 'rb') as fobj:
            viceroy = fobj.read()
        with open(os.path.join(STATIC, 'viceroy.html'), 'rb') as fobj:
            html = fobj.read()
        self.urls = {
            '/': (html, 'text/html'),
            '/viceroy.js': (viceroy, 'application/javascript'),
            '/tests.js': (javascript.encode('utf8'), 'application/javascript')
        }
        self.thread = None
        self.port = None
        self.port_event = threading.Event()
        self.done_event = threading.Event()

    def wait(self, timeout=5):
        done = self.done_event.wait(timeout)
        print('done')
        if done:
            print('done!')
            return self.thread.result
        else:
            print('fail')
            return Result(True, 'VICEROY:INTERNAL:Timeout')

    def stop(self):
        print('stop')
        if self.thread is not None:
            self.thread.terminate()
            self.thread.join()

    def run_async(self, timeout=5):
        self.thread = ServerThread(
            self.port_event,
            self.done_event,
            self.urls
        )
        self.thread.daemon = True
        self.thread.start()
        self.port_event.wait(timeout)
        self.port = self.thread.port


class ViceroyTestCase(unittest.TestCase):
    server_class = Server
    url = '/'

    def get_driver(self):
        from selenium.webdriver.firefox import webdriver
        return webdriver.WebDriver()

    @contextlib.contextmanager
    def run_server(self, javascript):
        server = self.server_class(javascript)
        try:
            server.run_async()
            yield server
        finally:
            server.stop()

    def assertInBrowser(self, javascript):
        driver = self.get_driver()
        try:
            with self.run_server(javascript) as server:
                driver.get('http://localhost:{}{}'.format(
                    server.port, self.url
                ))
                result = server.wait()
                if result.failed:
                    self.fail(result.error)
        finally:
            driver.quit()


class QUnitTestCase(ViceroyTestCase):
    pass


class JasmineTestCase(ViceroyTestCase):
    pass
