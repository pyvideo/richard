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


Get richard
===========

Clone the repository from github::

    $ git clone git://github.com/willkg/richard.git


Install Python requirements
===========================

Now you need to install some other things all of which are specified
in the requirements files provided.

Create a virtual environment::

    $ cd richard
    $ virtualenv ./venv/

Make sure to activate the virtual environment every time you go to use
richard things. You can do that like this::

    $ ./venv/bin/activate

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


Configure
=========

You need to create a ``settings_local.py`` file. To do that, do this::

    # cp richard/settings_local.py-dist richard/settings_local.py


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

If you want to set up some initial data, do::

    $ ./manage.py generatedata

This is useful to see how the site works.


Run the tests
=============

Richard uses ``django-nose`` to discover tests.

Activate the virtual environment, then run the tests::

    $ ./manage.py test --nologcapture --nocapture


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
