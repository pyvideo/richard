================================
 Installing richard for hacking
================================

This covers how to clone richard and set it up for easy hacking.

.. Note::

   richard is pretty new and is under heavy development. As such, the
   documentation for it sucks and the installation guide may have as
   much of a chance of helping you install richard as it does helping
   you make a quiche.

   I'm really sorry about that, but I'm still bootstrapping the
   project.


richard requires a bunch of stuff to run. I'm going to talk about this
stuff in two groups:

1. stuff that you should install with your package manager
2. Python packages that should get installed in a virtual environment


Things that you should install with your package manager
========================================================

You need the following things all of which should be provided by your
system/package manager:

* Python 2.6 or 2.7
* pip
* virtualenv


On Debian, this translates to::

    apt-get install \
        python \
        python-pip \
        python-virtualenv


Getting richard
===============

Clone the repository from github::

    $ git clone git://github.com/willkg/richard.git


Python packages to install
==========================

Now you need to install some other things all of which are specified
in the requirements files provided.

Create a virtual environment::

    $ cd richard
    $ virtualenv ./venv/

Activate the virtual environment::

    $ . ./venv/bin/activate

Use pip to install the development requirements::

    $ pip install -r requirements/development.txt

.. Note::

   pip installed the requirements into the virtual environment. You'll need
   to activate this virtual environment in order to run richard.  To activate
   the virtual environment, do::

       $ . ./venv/bin/activate

.. Note::

   If you want to use virtualenvwrapper or want to set things up differently,
   feel free to do so!


Setting up the database
=======================

To get started quickly you can use SQLite. It does not require any setup,
Django will handle things for you.

.. Note::

   richard is known to work under MySQL. If you want to use postgres or
   some other system, then please do and let me know if it works!


Configuration
=============

Default configuration for the project goes in ``richard/settings.py``.

You will need to override some of those settings for your
instance. To do that:

1. create a file ``richard/settings_local.py``
2. add configuration for your instance in that file

If you're developing on richard, you can use this sample
``settings_local.py`` which uses database settings from the example
database setup::

    DEBUG = True
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'path/to/database.file',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': ''
        }
    }


Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'

.. todo:: list configuration settings that should be in settings_local.py


Setting up database schema and creating admin user
==================================================

To set up the database schema and create the admin user, run::

    $ ./manage.py syncdb --migrate

The admin user account you create here can be used to log into the richard
admin section.


Setting up sample data (optional)
=================================

If you want to set up some initial data, do::

    $ ./manage.py loaddata sample_data.json

This is useful to see how the site works.


Running richard
===============

To run richard, make sure your virtual environment is activated and then::

    $ ./manage.py runserver
