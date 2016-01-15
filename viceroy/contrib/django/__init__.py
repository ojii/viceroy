import contextlib

import django
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from viceroy.api import ViceroyTestCase


class ViceroyDjangoTestCase(ViceroyTestCase, StaticLiveServerTestCase):
    @classmethod
    @contextlib.contextmanager
    def viceroy_server(cls):
        yield cls.server_thread.port

    @classmethod
    def setUpClass(cls):
        django.setup()
        settings.VICEROY_TESTING = True
        super(ViceroyDjangoTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(ViceroyDjangoTestCase, cls).tearDownClass()
        settings.VICEROY_TESTING = False
