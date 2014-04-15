from http import server
import json
import multiprocessing
import mimetypes
import collections
import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASEDIR, 'static')
Result = collections.namedtuple('Result', 'failed message')


def static(path, content_type=None):
    with open(path, 'rb') as fobj:
        data = fobj.read()
    if content_type is None:
        content_type, _ = mimetypes.guess_type(path)
    if content_type is None:
        raise TypeError(
            "Could not figure out content type of {!r}".format(path)
        )
    return data, content_type


class RequestHandler(server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        response, content_type = self.server_process.urls.get(
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
            length = int(self.headers['Content-Length'])
            raw_data = self.rfile.read(length)
            result = json.loads(raw_data.decode('utf8'))
            self.server_process.notify(result['failed'], result['message'])
            self._send(200, b'', 'text/plain')
        else:
            self._send(404, b'', 'text/plain')

    def _send(self, status, response, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)


class ServerProcess(multiprocessing.Process):
    def __init__(self, port_event, port_value, result_queue, urls):
        self.port_event = port_event
        self.port_value = port_value
        self.result_queue = result_queue
        self.httpd = None
        self.urls = urls
        super().__init__(daemon=True)

    def run(self):
        handler_class = type(
            'Handler',
            (RequestHandler,),
            {'server_process': self}
        )
        address = ('localhost', self.port_value.value)
        self.httpd = server.HTTPServer(address, handler_class)
        self.port_value.value = self.httpd.server_port
        self.port_event.set()
        self.httpd.serve_forever()

    def shutdown(self):
        if self.httpd is not None:
            self.httpd.shutdown()
            self.httpd.server_close()

    def notify(self, failed, message):
        self.result_queue.put(Result(failed, message))
        self.shutdown()


class Server(object):
    index_html_path = os.path.join(STATIC, 'viceroy.html')

    def __init__(self, javascript):
        self.urls = {}
        self.setup_default_urls()
        self.setup_javascript_url(javascript)
        self.setup_extra_urls()
        self.process = None
        self.port = None
        self.port_event = multiprocessing.Event()
        self.port_value = multiprocessing.Value('i', 0)
        self.result_queue = multiprocessing.Queue()

    def setup_default_urls(self):
        self.urls.update({
            '/': static(self.index_html_path),
            '/viceroy.js': static(os.path.join(STATIC, 'viceroy.js')),
        })

    def setup_javascript_url(self, javascript):
        self.urls.update({
            '/tests.js': (javascript.encode('utf8'), 'application/javascript')
        })

    def setup_extra_urls(self):
        pass

    def wait(self, timeout=5):
        return self.result_queue.get(True, timeout)

    def stop(self):
        if self.process is not None:
            self.process.shutdown()
            self.process.terminate()

    def run_async(self, timeout=5):
        if self.process is not None:
            self.process.stop()
        self.process = ServerProcess(
            self.port_event,
            self.port_value,
            self.result_queue,
            self.urls
        )
        self.process.start()
        if self.port_event.wait(timeout):
            self.port = self.port_value.value
        else:
            raise Exception("Could not get port from server process")


class QUnitServer(Server):
    index_html_path = os.path.join(STATIC, 'qunit', 'tests.html')

    def setup_extra_urls(self):
        qunit = lambda *bits: os.path.join(STATIC, 'qunit', *bits)
        self.urls.update({
            '/qunit/qunit.js': static(qunit('qunit.js')),
            '/qunit/viceroy-bridge.js': static(qunit('viceroy-bridge.js')),
        })


class JasmineServer(Server):
    index_html_path = os.path.join(STATIC, 'jasmine', 'tests.html')

    def setup_extra_urls(self):
        jasmine = lambda *bits: os.path.join(STATIC, 'jasmine', *bits)
        self.urls.update({
            '/jasmine/boot.js': static(jasmine('boot.js')),
            '/jasmine/jasmine.js': static(jasmine('jasmine.js')),
            '/jasmine/jasmine-html.js': static(jasmine('jasmine-html.js')),
            '/jasmine/viceroy-bridge.js': static(jasmine('viceroy-bridge.js')),
        })
