# Django settings for richard project.
from configurations import Configuration, values

# ===================================================
# NOTE: Override settings for local instances in the
# richard/settings_local.py module.
# ===================================================

import imp
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Base(Configuration):
    ##########
    # App configuartion
    ##########
    DJANGO_APPS = (
        'django.contrib.auth',
        'django_browserid',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.redirects',
        'django.contrib.sitemaps',
    )

    THIRD_PARTY_APPS = (
        'grappelli',
        'haystack',
        'south',
        'rest_framework',
        'rest_framework.authtoken',
    )

    LOCAL_APPS = (
        'richard.base',
        'richard.notifications',
        'richard.pages',
        'richard.suggestions',
        'richard.videos',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    ##########
    # End App configuartion
    ##########

    ##########
    # Middleware Configuration
    ##########
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
    ##########
    # End Middleware Configuration
    ##########

    ##########
    # Debug
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.Value(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    ##########
    # End Debug
    ##########

    ##########
    # Secret Configuration
    ########
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = values.Value('secret-value')
    ##########
    # End Secret Configuration
    ##########

    ##########
    # Fixture Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    # Don't use them though...
    FIXTURE_DIRS = (
        os.path.join(BASE_DIR, 'fixtures'),
    )
    ##########
    # End Fixture Configuration
    ##########


    ##########
    # Manager Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS
    ##########
    # End Manager Configuration
    ##########

    ##########
    # Database Configuration
    ##########
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    # with syntax from
    # https://github.com/kennethreitz/dj-database-url
    DATABASES = values.DatabaseURLValue('sqlite:///' + os.path.join(BASE_DIR, 'database.db'))
    ##########
    # End Database Configuration
    ##########

    ##########
    # General Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'America/Chicago'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'en-us'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = False

    ##########
    # End General Configuration
    ##########

    ##########
    # Template Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.csrf',
        'django.core.context_processors.i18n',
        'django.core.context_processors.static',
        "django.core.context_processors.request",

        'richard.base.context_processors.base',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    ##########
    # End Template Configuration
    ##########

    ##########
    # Static File Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
    )
    ##########
    # End Static File Configuration
    ##########

    ##########
    # Media Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    ##########
    # End Media Configuration
    ##########

    ##########
    # URL Configuration
    ##########
    ROOT_URLCONF = 'richard.config.urls'

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'richard.config.wsgi.application'
    ##########
    # End URL Configuration
    ##########

    ##########
    # Authentication Configuration
    ##########
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_browserid.auth.BrowserIDBackend',
    )
    ##########
    # End Authentication Configuration
    ##########

    ##########
    # Logging Configuration
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
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
    ##########
    # End Logging Configuration
    ##########

    ##########
    # Richard-specific settings
    ##########

    # site_url is the url for this site. it's important it's
    # correct otherwise browserid authentication won't work.
    SITE_URL = values.URLValue('http://127.0.0.1:8000', environ_prefix='RICHARD')
    LOGIN_URL = '/'
    LOGIN_REDIRECT_URL = '/'
    LOGIN_REDIRECT_URL_FAILURE = '/login-failure'

    # Title of your site here
    SITE_TITLE = u'richard'
    GRAPPELLI_ADMIN_TITLE = u'Richard Admin'

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
    API = values.BooleanValue(False, environ_prefix='RICHARD')

    # Modify this list to prevent spam messages in public suggestions
    SPAM_WORDS = []

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
        },
    }

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSON_CLASSES': (
            'rest_framework.permissions.IsAdminUser',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        ),
        'PAGINATE_BY': 20
    }
    ##########
    # End Richard-specific settings
    ##########


class Testing(Base):
    DEBUG = True
    INSTALLED_APPS = Base.INSTALLED_APPS
    SECRET_KEY = 'richard-testing'
    DATABASES = values.DatabaseURLValue('sqlite://:memory:')

    API = True

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(BASE_DIR, '_test_whoosh_index'),
        },
    }

    try:
        # Add django_nose for testing but only if it's installed.
        imp.find_module('django_nose')
        INSTALLED_APPS = tuple(list(INSTALLED_APPS) + ['django_nose'])
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    except ImportError:
        pass


class Dev(Base):
    API = values.BooleanValue(True, environ_prefix='RICHARD')
    DEBUG = True

    SECRET_KEY = 'richard-testing'

    AUTHENTICATION_BACKENDS = (
        'richard.base.auth.AutoLoginBackend',  # DON'T use this in Production!
        'django_browserid.auth.BrowserIDBackend',
    )

    BROWSERID_AUTOLOGIN = ''


class Prod(Base):
    SECRET_KEY = values.SecretValue()
