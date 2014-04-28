from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import index

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^viceroy/', include('viceroy.contrib.django.urls')),
    url(r'^static/', include(staticfiles_urlpatterns())),
)
