=======
 Tests
=======


.. contents::
   :local:


Testing requirements
====================

richard uses ``django-nose`` to tie the Django test system to ``nose``.

I like to additionally use ``nose-progressive`` because it makes the test
output more useful.


Running tests
=============

To run the tests, make sure your virtual environment is activated and then::

    ./manage.py test

To run the tests with nose-progressive::

    ./manage.py test --with-progressive


Add new tests
=============

Locations
---------

Tests for apps go in ``richard/richard/APPNAME/tests/``.

Tests for richard project go in ``richard/richard/tests/``.


Conventions
-----------

Modules should be named ``test_*.py``.

Classes should be named ``Test*`` and should extend Django's
``UnitTest`` class.

Functions and methods should be named ``test_*``.

Use the non-camel-case versions of ``assertXyz`` and friends if they
exist, but it's probably better to use nose's ``eq_`` and Python's
``assert``.

See existing tests for examples.

We're not shooting for 100% code coverage---only write tests that are
compelling.

Make sure tests are documented and it's clear what's being tested and
how.
