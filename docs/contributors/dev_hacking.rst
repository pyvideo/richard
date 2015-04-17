.. _hacking-chapter:

=========================================
 Installing, running and testing richard
=========================================

This covers how to clone richard and set it up for easy hacking.

.. Note::

   richard is pretty new and is under heavy development. As such, the
   documentation for it sucks and the installation guide may have as
   much of a chance of helping you install richard as it does helping
   you make a quiche.

   I'm really sorry about that, but I'm still bootstrapping the
   project.


.. contents::
   :local:


richard requires a bunch of stuff to run. I'm going to talk about this
stuff in two groups:

1. stuff that you should install with your package manager
2. Python packages that should get installed in a virtual environment


Install things with your package manager
========================================

You need the following things all of which should be provided by your
system/package manager:

* Python 2.7
* pip
* virtualenv


On Debian, this translates to::

    $ apt-get install \
          libxml2 \
          libxml2-dev \
          libxslt-dev \
          python-pip \
          python-virtualenv

On Fedora, this translates to::

    $ yum install \
          libxml2-devel \
          libxslt-devel \
          python-pip \
          python-virtualenv


Get richard
===========

Clone the repository from github::

    $ git clone git://github.com/pyvideo/richard.git


Install Python requirements
===========================

Now you need to install some other things all of which are specified
in the requirements files provided.

Create a virtual environment::

    $ cd richard
    $ virtualenv ./venv/

Make sure to activate the virtual environment every time you go to use
richard things. You can do that like this::

    $ . ./venv/bin/activate

Use pip to install the development requirements::

    $ ./venv/bin/pip install -e .\[dev\]

**(Optional)** If you want to also install with postgres support::

    $ apt-get install \
        postgresql \
        build-essential \
        libpq-dev \
        python-dev
    $ ./venv/bin/pip install -e .\[dev,postgresql\]


.. Note::

   If you want to use virtualenvwrapper or want to set things up differently,
   feel free to do so!


Install the pre-commit hooks
============================

richard uses `pre-commit <http://pre-commit.com/>`_ package to install
various pre-commit hooks to lint the code. Install the hooks by running::

    $ pre-commit install

The configuration of the hooks is done in ```.pre-commit-config.yaml``.
To ignore the errors and proceed with the commit, use the ```--no-verify```
option to the ```git commit``` command.


Configure
=========

You need to create a ``settings_local.py`` file. To do that, do this::

    $ cp richard/settings_local.py-dist richard/settings_local.py


The settings should work out of the box, but you can change them as
you see fit.

**(Optional)** If you want to use postgres, uncomment the postgres
line in the ``DATABASES`` section.


Set up database schema and create superuser
===========================================

To set up the database schema and create the superuser, run::

    $ ./manage.py syncdb --migrate

The superuser account you create here can be used to log into the
richard admin section.


Set up sample data (optional)
=============================

You can add some sample data to your database which makes development
a little easier since you can see what things look like. To do this,
do::

    $ ./manage.py generatedata

This doesn't affect tests at all. You can remove the sample data at
some later point. Running ``generatedata`` a second time will fail
because slugs won't be unique.


Run the tests
=============

Richard uses `pytest-django <http://pytest-django.readthedocs.org/en/latest/>`_
to discover tests.

Activate the virtual environment, then run the tests::

    $ py.test ./tests/


Run the server
==============

Run the server like this::

    $ ./manage.py runserver --traceback


Then point your browser at ``http://localhost:8000/``.


Troubleshooting
===============

I can't log in
--------------

First, make sure your administrator account has an email address
associated with it. This is the email address you will log in with
Persona.

Second, if you're seeing a "Misconfigured" kind of error, make sure
the ``SITE_URL`` in your ``settings_local.py`` file matches the domain
and port that the server is running on. If it doesn't match, then
django-browserid won't work.

See `the django-browserid troubleshooting docs
<https://django-browserid.readthedocs.org/en/latest/details/troubleshooting.html>`_
for more details.
