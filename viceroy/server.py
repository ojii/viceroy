from contextlib import contextmanager
import multiprocessing
import os


try:
    from http import server
except ImportError:
    import SimpleHTTPServer as server


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

    # def log_date_time_string(self):
    #     pass
    #
    # def log_error(self, format, *args):
    #     pass
    #
    # def log_message(self, format, *args):
    #     pass
    #
    # def log_request(self, code='-', size='-'):
    #     pass


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
