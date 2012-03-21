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

   If you have thoughts on better instructions, let me know.


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


Setting up the database
=======================

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

.. Note::

   If you want to use postgres or some other system, then please do and
   let me know if it works!


Configuration
=============

Default configuration for the project is in ``richard/richard/settings.py``.

You can either copy that into ``your_site`` and edit it there or
create a ``settings_site.py`` file, import the defaults and override
the ones you want to override.

Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'


.. todo:: list configuration settings that should be in settings file


Setting up database schema and creating admin user
==================================================

To set up the database schema and create the admin user, run::

    $ ./manage.py syncdb

The admin user account you create here can be used to log into the richard
admin section.


Setting up sample data (optional)
=================================

If you want to set up some initial data, do::

    $ ./manage.py loaddata sample_data.json

This is useful to see how the site works.


Setting up your server
======================

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
