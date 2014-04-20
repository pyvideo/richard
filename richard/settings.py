# Django settings for richard project.

# ===================================================
# NOTE: Override settings for local instances in the
# richard/settings_local.py module.
# ===================================================

import imp
import os
import sys

# site_root is the parent directory
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

# site_url is the url for this site. it's important it's
# correct otherwise browserid authentication won't work.
SITE_URL = 'http://127.0.0.1:8000'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/login-failure'

# root is this directory
ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# Title of your site here
SITE_TITLE = u'richard'
GRAPPELLI_ADMIN_TITLE = u'Richard Admin'

MANAGERS = ADMINS


# =========================
# Richard-specific settings
# =========================

# See the configuration documentation for more details on these
# settings.

# This dictates whether django-browserid will create new users or not
# when people log in that it doesn't have a record for.
BROWSERID_CREATE_USER = False

# Verification class for django-browserid.
BROWSERID_VERIFY_CLASS = 'richard.base.browserid.RichardVerify'

# The (width, height) to use when you tell richard to pull down remote
# thumbnails, resize them, and store them locally.
VIDEO_THUMBNAIL_SIZE = (160, 120)

# Order that media items get sorted.
MEDIA_PREFERENCE = ('ogv', 'webm', 'mp4', 'flv',)

# List of "static pages". See the documentation for setting up a page.
PAGES = ['about']

# Feed size for Newly Updated Videos feed.
MAX_FEED_LENGTH = 30

# Whether or not to enable opensearch suggestions for search.  Note:
# Enabling this can cause a lot of work on your search system. If you
# enable this, keep an eye on your system performance.
OPENSEARCH_ENABLE_SUGGESTIONS = False

# Whether or not to enable Amara Universal Subtitles site-wide.
# http://www.universalsubtitles.org/en/
AMARA_SUPPORT = False

# Whether or not to enable the REST API. See the documentation for
# more about the API.
API = False


DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(SITE_ROOT, 'database.db'),

        # The following settings are not used with sqlite3.
        'USER': '',
        'PASSWORD': '',
        # Set to empty string for localhost.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(SITE_ROOT, 'whoosh_index'),
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Fixture directory for easy bulk-loading
FIXTURE_DIRS = (
    os.path.join(ROOT, 'fixtures'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'richard.base.middleware.BrowserDetectMiddleware',

    # This should probably be last. It catches 404 errors, then checks
    # to see if we should be redirecting the url.
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'richard.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'richard.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    "django.core.context_processors.request",

    'richard.base.context_processors.base',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django_browserid',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'haystack',
    'south',
    'rest_framework',
    'rest_framework.authtoken',
    'eadred',

    'richard.base',
    'richard.notifications',
    'richard.pages',
    'richard.suggestions',
    'richard.videos',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
)

try:
    # Add django_nose for testing but only if it's installed.
    imp.find_module('django_nose')
    INSTALLED_APPS = tuple(list(INSTALLED_APPS) + ['django_nose'])
except ImportError:
    pass

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSON_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGINATE_BY': 20
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Modify this list to prevent spam messages in public suggestions
SPAM_WORDS = []

try:
    from richard.settings_local import *
except ImportError:
    pass


if 'test' in sys.argv:
    try:
        from richard.settings_test import *
    except ImportError:
        pass
