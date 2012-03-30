=======
 Tests
=======

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

Tests for apps go in ``richard/apps/APPNAME/tests/``.

Tests for richard project go in ``richard/richard/tests/``.

Modules should be named ``test_*.py``.

Functions should be named ``test_*``.

Classes should be named ``Test*``.

See existing tests for examples.
