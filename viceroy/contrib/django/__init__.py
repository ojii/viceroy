import contextlib

from django.conf import settings
from django.test import LiveServerTestCase

from viceroy.api import ViceroyTestCase


class ViceroyDjangoTestCase(ViceroyTestCase, LiveServerTestCase):
    @classmethod
    @contextlib.contextmanager
    def viceroy_server(cls):
        yield cls.server_thread.port

    @classmethod
    def setUpClass(cls):
        settings.VICEROY_TESTING = True
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        settings.VICEROY_TESTING = False
