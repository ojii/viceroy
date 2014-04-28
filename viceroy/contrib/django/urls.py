from django.conf.urls import patterns
from django.conf.urls import url

from .views import serve_viceroy

urlpatterns = patterns('',
    url(r'^(?P<path>.*)', serve_viceroy)
)
