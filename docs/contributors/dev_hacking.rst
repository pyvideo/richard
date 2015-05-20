.. _hacking-chapter:

=======================================
Installing, running and testing richard
=======================================

This covers how to clone richard and set it up for easy hacking.

.. Note::

   richard is still under heavy development. As such, the documentation
   for it is constantly in flux and probably outdated and the installation
   guide may have as much of a chance of helping you install richard
   as it does helping you make a quiche.

   I'm really sorry about that. If you find issues, please let us know:

   https://github.com/pyvideo/richard/issues


.. contents::
   :local:


richard requires a bunch of stuff to run. I'm going to talk about this
stuff in two groups:

1. stuff that you should install with your operating system's package
   manager
2. Python packages that you should install with pip in a virtual
   environment


Install things with your package manager
========================================

You need the following things all of which should be provided by your
system/package manager:

* Python 2.7 or 3.3+
* pip
* virtualenv
* git


Python 2.7
----------

Debian::

    $ apt-get install \
          libxml2 \
          libxml2-dev \
          libxslt-dev \
          python-pip \
          python-virtualenv

Fedora::

    $ yum install \
          libxml2-devel \
          libxslt-devel \
          python-pip \
          python-virtualenv


Python 3.3+
-----------

FIXME: Please provide instructions.


Install and configure richard
=============================

Get the code, set up virtual environment and install requirements
-----------------------------------------------------------------

First, you need the code. Clone the repository from github::

    $ git clone git://github.com/pyvideo/richard.git


Create a virtual environment::

    $ cd richard
    $ virtualenv ./venv/


.. Note::

   If you want to use virtualenvwrapper or want to set things up differently,
   feel free to do so!


Make sure to activate the virtual environment every time you go to use
richard things. You can do that like this::

    $ . ./venv/bin/activate

Use pip in the virtual environment to update pip to the latest version::

    $ pip install -U pip

Use pip in the virtual environment to install richard and the development
requirements::

    $ pip install -e ".[dev]"

**(Optional) use postresql**

    If you want to also install with postgres support, you'll need to install
    postgresql and the bits you need to compile the postgresql driver.

    On Debian::

        $ apt-get install \
            postgresql \
            build-essential \
            libpq-dev \
            python-dev

    Then run in your virtual environment::

        $ pip install -e ".[postgresql]"


Configure
---------

You should be able to use the ``Dev`` configuration specified in
``richard.config.settings``. This is the default used by ``manage.py``.

The settings should work out of the box, but you can change them as
you see fit.

**(Optional) use postgres**

    Set the ``DATABASE_URL`` environment variable. See
    http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    for details.


Set up database schema
----------------------

To set up the database schema and create the superuser, run::

    $ ./manage.py migrate


Set up superuser account
------------------------

To create a superuser account, run::

    $ ./manage.py createsuperuser

The username and password don't matter--you'll never use
them. However, the email address you use does since that needs to be
the same as your Persona account.


All set!
--------

You should have richard installed now. Any time you update the richard
code, you'll want to install any requirements changes::

    $ pip install -e ".[dev]"

and run migrations::

    $ ./manage.py migrate


Run the tests
=============

Richard uses `pytest-django <http://pytest-django.readthedocs.org/en/latest/>`_
to discover tests.

Activate the virtual environment, then run the tests::

    $ py.test tests


Run the server
==============

Run the server like this::

    $ ./manage.py runserver --traceback


Then point your browser at ``http://localhost:8000/``.


Install the pre-commit hooks (optional)
=======================================

richard uses `pre-commit <http://pre-commit.com/>`_ package to install
various pre-commit hooks to lint the code when you create new commits.
Install the hooks by running::

    $ pre-commit install

The configuration of the hooks is done in ``.pre-commit-config.yaml`.
To ignore all the errors and proceed with the commit, use the
``--no-verify`` option to the ``git commit`` command. To ignore specifc
hooks, you can specify a comma-separated list of hook ids (available in
``.pre-commit-config.yaml``) in the environment variable ``SKIP``.


Set up sample data (optional)
=============================

You can add some sample data to your database which makes development
a little easier since you can see what things look like. To do this,
do::

    $ ./manage.py generatedata

.. Note::

   This doesn't affect running tests at all. You can always delete
   sample data later.

   FIXME: Running ``generatedata`` a second time will fail because slugs
   won't be unique.


Troubleshooting
===============

I can't log in
--------------

First, make sure your administrator account has an email address
associated with it. This is the email address you will log in with
Persona.

After that, wee `the django-browserid troubleshooting docs
<https://django-browserid.readthedocs.org/en/latest/user/troubleshooting.html>`_
for more details.
