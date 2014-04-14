# This is a sample settings_local.py file. To use it, do:
#
# 1. cp settings_local.py-dist settings_local.py
# 2. edit with your editor
#
# See settings.py and documentation for other things you can configure.

import os


# site_root is the parent directory
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

DEBUG = TEMPLATE_DEBUG = True

SECRET_KEY = 'secret key'

DATABASES = {
    'default': {
        # postgresql configuration
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_site',    # db name
        'USER': 'richard',
        'PASSWORD': 'richard',
        'HOST': 'localhost',
        'PORT': ''

        # This is a sqlite3 configuration. If you are a contributor
        # and don't have postgresql on your machine, then feel free
        # to comment out the previous lines and uncomment out the next
        # 6 lines:
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(SITE_ROOT, 'database.db'),
        # 'USER': '',
        # 'PASSWORD': '',
        # 'HOST': '',
        # 'PORT': '',
    }
}

# If you're doing development work and you're not in production and you have no
# Internet connection, uncomment the following and set BROWSERID_AUTOLOGIN to
# the email address of the account you want to log in as."

#AUTHENTICATION_BACKENDS = (
#    'richard.base.auth.AutoLoginBackend',
#    'django_browserid.auth.BrowserIDBackend',
#)
#
#BROWSERID_AUTOLOGIN = ''
