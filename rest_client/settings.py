try:
    from django.conf import settings as django_settings
except ImportError:
    HAS_DJANGO = False
else:
    HAS_DJANGO = True


if HAS_DJANGO:
    REST_CLIENT_SETTINGS = getattr(django_settings, 'django_settings', {})
else:
    REST_CLIENT_SETTINGS = {}


REST_CLIENT_SETTINGS['EXAMPLE'] = {
    'default': {
        'HOSTNAME': '127.0.0.1',
        'PORT': 8000
    }
}
