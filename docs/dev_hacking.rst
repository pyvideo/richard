=====================
 Install for hacking
=====================

This covers how to clone richard and set it up for easy hacking.

.. Note::

   Richard is pretty new and is under heavy development. As such, the
   documentation for it sucks and the installation guide may have as
   much of a chance of helping you install Richard as it does helping
   you make a quiche.

   I'm really sorry about that, but I'm still bootstrapping the
   project.


Richard requires a bunch of stuff to run. I'm going to talk about this
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
* MySQL Server
* MySQL client headers


On Debian, this translates to::

    apt-get install \
        python \
        python-pip \
        python-virtualenv \
        mysql-server \
        mysql-client \
        libmysqlclient-dev


Python packages to install
==========================

Now you need to install some other things all of which are specified
in the requirements files provided.

Using pip, create a virtual environment and install everything into
it::

    $ pip install -E ./venv/ -r requirements/base.txt

(Optional) If you plan on doing development work, running tests,
building documentation or something along those lines, then do::

    $ pip install -E ./venv/ -r requirements/development.txt

.. Note::

   This created a virtual environment. You'll need to use that virtual
   environment to run Richard. To activate the virtual environment, do::

       $ . ./venv/bin/activate


Setting up the database
=======================

You need to create a database and a user for that database.

For example, to create a database named ``richard`` with a user named
``richard`` with password ``password``, you'd do::

    $ mysql -u root -p
    mysql> CREATE DATABASE richard;
    mysql> GRANT ALL ON richard.* TO richard@localhost IDENTIFIED BY
        'password';

(Optional) If you're a developer and plan to run the test suite,
you'll also need to add permissions to the test database. The test
database has the same name as the database prepended with ``test_``.
For example::

    $ mysql -u root -p
    mysql> GRANT ALL ON test_richard.* TO richard@localhost IDENTIFIED
        BY 'password';


.. todo:: how to create the initial schema

.. todo:: how to load sample data


Configuration
=============

Default configuration for the project goes in ``richard/settings.py``.

You will need to override some of those settings for your
instance. To do that:

1. create a file ``richard/settings_local.py``
2. add configuration for your instance in that file

If you're developing on Richard, you can use this sample
``settings_local.py`` which uses database settings from the example
database setup::

    DEBUG = True
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'richard',
            'USER': 'richard',
            'PASSWORD': 'password',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        }
    }


Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'

.. todo:: create admin user

.. todo:: list configuration settings that should be in settings_local.py
