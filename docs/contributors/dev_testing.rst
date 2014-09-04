=======
 Tests
=======


.. contents::
   :local:


Testing requirements
====================

richard uses `pytest-django <http://pytest-django.readthedocs.org/en/latest/>`_
to tie the Django test system to `pytest <http://pytest.org/latest/>`_.

We use `FactoryBoy <http://factoryboy.readthedocs.org/en/latest/>`_ to
generate model instances and test data.


Running tests
=============

To run the tests, make sure your virtual environment is activated and
then::

    py.test tests/

You can see more options by doing::

    py.test --help

Once you get a runline you like, put it in a bash script.


Add new tests
=============

Locations
---------

Tests go in directories like ``tests/test_<APPNAME>/``.


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
