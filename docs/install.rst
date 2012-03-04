====================
 Installing richard
====================

.. Note::

   Richard is pretty new and is under heavy development. As such, the
   documentation for it sucks and the installation guide may have as
   much of a chance of helping you install Richard as it does helping
   you make a quiche.

   I'm really sorry about that, but I'm still bootstrapping the
   project.

   If you have thoughts on better instructions, let me know.


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


Setting up a directory structure
================================

Your site is an instance of richard with configuration, templates, and
data that's specific to your site.

I suggest something like the following::

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

    $ mkdir -p your_site \
          your_site/bin \
          your_site/templates \
          your_site/media \
          your_site/venv

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

Using pip, create a virtual environment and install everything into
it::

    $ pip install -E ./venv/ -r requirements/base.txt


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

Default configuration for the project is in ``richard/richard/settings.py``.

You can either copy that into ``your_site`` and edit it there or
create a ``settings_site.py`` file, import the defaults and override
the ones you want to override.

Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'


.. todo:: list configuration settings that should be in settings file

.. todo:: create admin user

.. todo:: template for production deployments


Upgrading
=========

This is a stub.

.. todo:: write upgrade documentation
