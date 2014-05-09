from django.conf import settings
from django.http import Http404
from django.views.static import serve

from viceroy.constants import VICEROY_STATIC_ROOT


def serve_viceroy(request, path):
    if not getattr(settings, 'VICEROY_TESTING', False):
        raise Http404()
    if path.endswith('/'):
        path = path[:-1]
    return serve(request, path, VICEROY_STATIC_ROOT)
