====================
 Installing richard
====================

.. Note::

   richard is pretty new and is under heavy development. As such, the
   documentation for it sucks and the installation guide may have as
   much of a chance of helping you install richard as it does helping
   you make a quiche.

   I'm really sorry about that, but I'm still bootstrapping the
   project.

   If you have thoughts on better instructions, let us know on the irc
   channel or write up an issue in the tracker.  See the
   :doc:`Contributor's Guide <../index>` for more details.


richard requires a bunch of stuff to run. I'm going to talk about this
stuff in two groups:

1. stuff that you should install with your package manager
2. Python packages that should get installed in a virtual environment


Things that you should install with your package manager
========================================================

You need the following things all of which should be provided by your
system's package manager:

* Python 2.6 or 2.7
* pip
* virtualenv


On Debian, this translates to::

    $ apt-get install \
          python \
          python-pip \
          python-virtualenv


Setting up a directory structure
================================

Your site is an instance of richard with configuration, templates, and
data that's specific to your site.

I suggest a directory hierarchy along the lines of the following::

    your_site/       <-- your site directory
    |- bin/          <-- directory for your .wsgi file
    |- templates/    <-- your site-specific templates
    |- media/        <-- images, js, css served by your web server
    |- venv/         <-- virtual environment holding
    |
    |- richard/      <-- tarball / git repository
       |- richard/   <-- richard django project
    ...

To generate that::

    $ mkdir your_site
    $ cd your_site
    $ mkdir bin templates media venv

If you have a tarball::

    $ cd your_site
    $ tar -xzvf richard.tar.gz

If you're cloning from git::

    $ cd your_site
    $ git clone git://github.com/willkg/richard.git


.. Note::

   The rest of these instructions assume your current working
   directory is ``your_site``.


Python packages to install
==========================

Now you need to install some other things all of which are specified
in the requirements files provided.

Create a virtual environment::

    $ cd your_site
    $ virtualenv ./venv/

Activate the virtual environment::

    $ . ./venv/bin/activate

Use pip to install the requirements::

    $ pip install -r richard/requirements/base.txt


.. Note::

   pip installed the requirements into the virtual environment. You'll need
   to activate this virtual environment in order to run richard.  To activate
   the virtual environment, do::

       $ . ./venv/bin/activate

.. Note::

   If you want to use virtualenvwrapper or want to set things up differently,
   feel free to do so!


Configuration
=============

Default configuration for the project is in
``richard/richard/settings.py``.

You can either copy that into ``your_site`` and edit it there or
create a ``settings_site.py`` file, import the defaults and override
the ones you want to override.

Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'


.. todo:: list configuration settings that should be in settings file


Setting up database
===================

Now you need to set up a database where richard will store its data.

* :ref:`install-chapter-mysql-db`
* :ref:`install-chapter-sqlite-db`
* :ref:`install-chapter-postgres-db`

We're really sorry if the database you want to use with richard isn't
in that list. If you need help, we'll do what we can. See
:ref:`contribute-project-details` for how to contact us for help.


.. _install-chapter-sqlite-db:

Setting up the database (sqlite)
--------------------------------

.. Warning::

   We don't encourage you to use sqlite for production, but if you
   must, you must.


Setting up sqlite is easy because the configuration for it is already
in the settings.py file. If you like the defaults, you're done!


.. _install-chapter-mysql-db:

Setting up the database (mysql)
-------------------------------

Requirements
^^^^^^^^^^^^

You need the following things from your system's package manager:

* MySQL Server
* MySQL client headers

On Debian, this translates to::

    $ apt-get install mysql-server mysql-client libmysqlclient-dev

You'll also need some Python packages::

    $ pip install -r richard/requirements/mysql_backend.txt


Creating database
^^^^^^^^^^^^^^^^^

You need to create a database and a user for that database.

For example, to create a database named ``richard`` with a user named
``richard`` with password ``password``, you'd do::

    $ mysql -u root -p
    mysql> CREATE DATABASE richard;
    mysql> CREATE USER richard@localhost IDENTIFIED BY 'password';
    mysql> GRANT ALL ON richard.* TO richard@localhost IDENTIFIED BY
        'password';

.. Note::

   (Optional) If you're a developer and plan to run the test suite,
   you'll also need to add permissions to the test database. The test
   database has the same name as the database prepended with ``test_``.
   For example::

       $ mysql -u root -p
       mysql> GRANT ALL ON test_richard.* TO richard@localhost IDENTIFIED
           BY 'password';


Configuration
^^^^^^^^^^^^^

In its default configuration, richard uses SQLite. To use your MySQL
database, edit your ``settings.py`` file and change the ``DATABASES``
configuration to something like this::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'richard',
            'USER': 'richard',
            'PASSWORD': 'richard',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        }
    }


.. _install-chapter-postgres-db:

Setting up the database (postgresql)
------------------------------------

.. todo:: Write setup for postgres.



Setting up database schema and creating admin user
==================================================

To set up the database schema and create the admin user, run::

    $ ./manage.py syncdb

The admin user account you create here can be used to log into the
richard admin section.

Then run::

    $ ./manage.py migrate

This sets up the rest of the database tables and also creates the save point
for migrations making it possible to upgrade your richard instance in the
future.


Setting up your web server
==========================

Apache and mod_wsgi
-------------------

http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango

A sample ``.wsgi`` file is in ``richard/`` in the repository.


Nginx and gunicorn
------------------

Create a file ``/etc/nginx/sites-available/your-site``:

.. todo:: finish writing nginx/gunicorn setup


Your favorite server combo here!
--------------------------------

Here!


Templates
=========

.. todo:: write up instructions for templates


Sitemap
=======

.. todo:: explain how to either point to sitemap in robots.txt or ping google,
          document how this works with other search engines
