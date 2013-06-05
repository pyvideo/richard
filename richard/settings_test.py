# Override settings for test environment here

import os

# site_root is the parent directory
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(SITE_ROOT, '_test_whoosh_index'),
    },
}

DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

# This allows the "test_api_disabled" test to kick off. The other api
# tests tweak things so they can run.
API = False

SECRET_KEY = 'richard-test'
