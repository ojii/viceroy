import contextlib
import multiprocessing
import socket
import time

from flask.ext.testing import TestCase

from viceroy.api import ViceroyTestCase


def _server_started(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', port))
    except ConnectionRefusedError:
        return False
    else:
        return True
    finally:
        sock.close()


class ViceroyFlaskTestCase(ViceroyTestCase, TestCase):
    viceroy_flask_app = None
    viceroy_flask_port = 5000

    def _pre_setup(self):
        pass

    def _post_teardown(self):
        pass

    @classmethod
    def viceroy_get_flask_app(cls):
        return cls.viceroy_flask_app

    @classmethod
    @contextlib.contextmanager
    def viceroy_server(cls):
        app = cls.viceroy_get_flask_app()
        app.config['TESTING'] = True
        port = cls.viceroy_flask_port
        app.config['LIVESERVER_PORT'] = port
        cls.viceroy_flask_process = None
        try:
            cls._start_flask_server(app)
            yield port
        finally:
            cls._stop_flask_server()

    @classmethod
    def _start_flask_server(cls, app):
        cls.viceroy_flask_process = multiprocessing.Process(
            target=app.run, kwargs={
                'port': cls.viceroy_flask_port
            }
        )
        cls.viceroy_flask_process.start()
        while not _server_started(cls.viceroy_flask_port):
            time.sleep(0.01)

    @classmethod
    def _stop_flask_server(cls):
        if cls.viceroy_flask_process is not None:
            cls.viceroy_flask_process.terminate()
            cls.viceroy_flask_process.join()
