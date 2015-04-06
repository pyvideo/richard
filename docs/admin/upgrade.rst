===========
 Upgrading
===========

Upgrading 0.1 to 0.2
====================

1. Uninstall South in your virtual environments.

2. Run ``./manage.py migrate --fake`` to mark all the migrations as
   having run because we switched from Django 1.6 with South to Django
   1.7 migration systems.


Up to 0.1
=========

.. Note::

   When you upgrade to a new version of richard, please please please
   read through the What's New notes for all the versions between what
   you're running and what you're upgrading to **BEFORE** you start your
   upgrade process.

The general list of things you need to do when you upgrade to a new
version is as follows:

1. backup your database.

2. backup your virtual environment and code.

Basically, you want to be able to go back to square 1 if something
goes awry. If you don't do this effectively and something does go
awry, you'll feel very irritated with yourself.

After doing that, you should:

1. upgrade the richard software

2. upgrade your virtual environment::

       $ pip install .

3. update your settings files---details on what needs to be updated
   will be in the What's New notes

4. upgrade your database::

       $ ./manage.py migrate

5. upgrade your index::

       $ ./manage.py rebuild_index

6. upgrade your templates---details on what needs to be updated will
   be in the What's New notes
