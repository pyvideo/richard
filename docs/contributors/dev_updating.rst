==================
 Updating richard
==================

If you're hacking on richard and running it from a git clone, then you'll
need to do the following periodically.


.. contents::
   :local:


Updating virtual environment
============================

Make sure you've activated your virtual environment.

Then::

    $ pip install -r requirements/develop.txt


.. Note::

   If you think you horked your virtual environment, just wipe it and
   build a new one.


Perform migrations
==================

richard uses `south <http://south.aeracode.org/>`_ to manage database
migrations.

To migrate your database to the latest schema, do::

    $ ./manage.py syncdb
    $ ./manage.py migrate


.. Note::

   If you're already up-to-date, then this won't do anything.
