from django.conf import settings


def viceroy(request):
    return {
        'VICEROY_TESTING': getattr(settings, 'VICEROY_TESTING', False)
    }
