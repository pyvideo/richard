====================
 Installing richard
====================

.. Note::

   richard is not heavily used. As such the documentation is
   lacking and the installation guide may have as much of a chance of
   helping you install richard as it does helping you make a quiche.
   I'm really sorry about that.

   If you have any problems or want to contribute fixes, open up an
   `issue on GitHub <https://github.com/willkg/richard/issues>`_ or talk
   to us on irc. See the :ref:`contribute-project-details` for more
   details.


.. contents::
   :local:


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


Getting richard
===============

You can download a zip file:

* v0.1: https://github.com/willkg/richard/archive/v0.1.zip
* bleeding edge in development: https://github.com/willkg/richard/archive/master.zip

If you're planning to contribute, then maybe it's better to clone the
repository with git::

    $ git clone git://github.com/willkg/richard.git


Setting up a directory structure
================================

Your site is an instance of richard with configuration, templates, and
data that's specific to your site.

I suggest a directory hierarchy along the lines of the following::

    richard/            # untarred tarball, git clone, etc
      |- docs/          # richard docs
      |- richard/       # richard django project code
      |- ...
      |
      |- bin/           # any site-specific scripts you need
      |- site/          # anything specific to your site
      |  |- templates/  # your site-specific templates
      |  |- static/     # your site-specific static files (images, css, js, ...)
      |
      |- venv/          # your virtual environment


To generate that::

    # untar richard tarball, git clone, or something like that
    # which creates a richard/ directory
    $ cd richard
    $ mkdir -p site site/templates bin


.. Note::

   The rest of these instructions assume your current working
   directory is the top-most richard directory.


Python packages to install
==========================

Now you need to install some other things all of which are specified
in the requirements files provided.

In the top-most richard directory, create a virtual environment,
activate it and install requirements::

    $ virtualenv ./venv/
    $ . ./venv/bin/activate
    $ pip install -r richard/requirements/base.txt


.. Note::

   pip installed the requirements into the virtual environment. You'll need
   to activate this virtual environment in order to run richard.  To activate
   the virtual environment, do::

       $ . ./venv/bin/activate


If you want to use virtualenvwrapper or want to set things up differently,
go for it!


Configuration
=============

Default configuration for the project is in ``richard/settings.py``.

Copy ``richard/settings_local.py-dist`` to
``richard/settings_local.py``.

``richard/settings_local.py`` will hold any configuration that is
specific to your site. In addition to the things that are in the file,
you can override any settings in ``richard/settings.py`` by specifying
them in ``richard/settings_local.py``.

Edit that file and follow the instructions in the configuration.

Make sure to set a ``SECRET_KEY``::

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long secret key'


Here are additional configuration settings:

``PAGES``

    List of strings indicating what content pages are available.

    Default: ``PAGES = ['about']``

    If you add new content pages, you need to add them to this
    list. This allows them to show up on your site and show up in the
    sitemap.


``AMARA_SUPPORT``

    True or False

    Default: ``AMARA_SUPPORT = False``

    Set this to ``True`` if you want to enable `Universal Subtitles
    <http://www.universalsubtitles.org/en/>`_. For HTML5 and YouTube
    embed videos using the old object embed code (not the new iframe
    embed code), it'll wrap it in a widget that displays subtitles
    that are hosted on the Universal Subtitles site.

    Wait... What's Amara? PCF changed the name of something, but I
    don't know whether it was the software or the service. So it's
    either called Amara or Universal Subtitles.


``BROWSERID_CREATE_USER``

    True or False

    Default: ``BROWSERID_CREATE_USER = False``

    Specifies whether or not a new account is created when someone
    logs into the site with a Persona account that the site has never
    seen before.


``SPAM_WORDS``

    Set this to a list of spam words in order to automatically check
    newly submitted suggestion for spam and mark the items as such.

    .. Note::

       You only have to specify the word once in lowercase. You don't
       need differently cased versions.

       e.g. "viagra" is fine. You don't need "viagra", "Viagra",
       "VIAGRA", etc.


``VIDEO_THUMBNAIL_SIZE``

    TODO - document this


``MEDIA_PREFERENCE``

    TODO - document this


``OPENSEARCH_ENABLE_SUGGESTIONS``

    TODO - document this


``API``

    Defaults to False.

    Set to True if you want to enable the API. See the
    :ref:`api-chapter` for more details.


.. todo:: list configuration settings that should be in settings file


Setting up database (postgresql)
================================

Now you need to set up a database where richard will store its data.

First install psycopg2::

    $ pip install psycopg2

Next, create the database and user role you're going to use. Update
the ``richard/settings_local.py`` with the values you pick.

.. todo:: instructions for running with Heroku and other PaaS systems


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

Your richard instance has a `sitemap.xml
<http://www.sitemaps.org/>`_. This helps search engines find all the
things on your richard instance.

The url for the ``sitemap.xml`` file for your richard instance is
``/sitemap.xml``.

There are a few ways you can "advertise" your ``sitemap.xml`` file to
search engines. Details are in `the sitemaps.org guide
<http://www.sitemaps.org/protocol.html#informing>`_.

We suggest you at least add this line to your ``robots.txt``::

    Sitemap: http://YOUR-DOMAIN/sitemap.xml
