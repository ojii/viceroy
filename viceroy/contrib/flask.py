import contextlib
import multiprocessing
import time

from flask.ext.testing import TestCase

from viceroy.api import ViceroyTestCase


class ViceroyFlaskTestCase(ViceroyTestCase, TestCase):
    viceroy_flask_app = None
    viceroy_flask_port = 5000

    def _pre_setup(self):
        pass

    def _post_teardown(self):
        pass

    @classmethod
    @contextlib.contextmanager
    def viceroy_server(cls):
        cls.viceroy_flask_app.config['TESTING'] = True
        port = cls.viceroy_flask_port
        cls.viceroy_flask_app.config['LIVESERVER_PORT'] = port
        cls.viceroy_flask_process = None
        try:
            cls._start_flask_server()
            yield port
        finally:
            cls._stop_flask_server()

    @classmethod
    def _start_flask_server(cls):
        cls.viceroy_flask_process = multiprocessing.Process(
            target=cls.viceroy_flask_app.run, kwargs={
                'port': cls.viceroy_flask_port
            }
        )
        cls.viceroy_flask_process.start()

        # we must wait the server start listening
        time.sleep(1)

    @classmethod
    def _stop_flask_server(cls):
        if cls.viceroy_flask_process is not None:
            cls.viceroy_flask_process.terminate()
