==========================
 Deploying a richard site
==========================

Deploying basics
================

Step 1:

    Install richard using the installation instructions if you haven't
    already.

Step 2:

    Configure richard by creating a settings file as described in the
    installation instructions if you haven't already.

Step 3:

    Setting up your site for being served by a web server in a
    production environment. This step is covered here.


Directory structure
-------------------

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


Apache and mod_wsgi
===================

http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango

A sample ``.wsgi`` file is in ``richard/`` in the repository.


Templates
=========
