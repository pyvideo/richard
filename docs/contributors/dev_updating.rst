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

    $ ./venv/bin/pip install -e ".[dev]"


.. Note::

   If you think you hosed your virtual environment, just wipe it and
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


Update pre-commit hooks
=======================

richard uses `pre-commit <http://pre-commit.com/>`_ package to install
various pre-commit hooks to lint the code. If there are any changes to the
pre-commit configuration in .pre-commit-config.yaml, update the hooks by
running::

    $ pre-commit install
