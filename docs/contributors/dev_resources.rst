===========
 Resources
===========

This chapter is a list of resources and notes that I thought would be
helpful to new people who want to contribute to this software. There's
also some design decisions and code conventions in here, too.


.. contents::
   :local:


Project scaffolding
===================

Settings
--------

richard has migrated to
`django-configurations <http://django-configurations.readthedocs.org/>`_
which makes settings in Django behave more like regular old class inheritance.
The classes ``Base``, ``Testing``, ``Dev`` and ``Prod`` in the ``settings.py``
module all handle the expected domains. You can override these by:

* creating a ``settings_local.py`` file
* ``from . import settings``
* creating your class (or creating a Dev / Prod class) and extending from
  ``settings.Base``
* Updating your deployment scripts to run ``manage.py --settings
  richard.config.settings_local``


Requirements / environments / deployment
----------------------------------------

* `virtualenv <http://pypi.python.org/pypi/virtualenv>`_ and
  `pip <http://pypi.python.org/pypi/pip>`_

  richard uses virtualenv and pip to build the environment for richard
  to run.

  Requirements are listed in the ``setup.py`` with ``extra_requires`` defined
  for local development and postgres. Since richard is meant for deployment
  rather than a framework, requirements are pinned hard. This makes it easy to
  install various options without having multiple requirements files.

Documentation
-------------

* `Sphinx <http://sphinx.pocoo.org/>`_ and
  `restructuredtext <http://docutils.sourceforge.net/rst.html>`_

  Documentation is in ``docs/`` and uses Sphinx for organizing and
  building it and restructuredtext for the markup.


Tools
=====

* `git <http://git-scm.com/>`_,
  `github <http://help.github.com/>`_ and
  `ProGit <http://progit.org/>`_

  richard uses git for version control. This has a big effect on how
  the project evolves in respects to code changes.

* `pyflakes <http://pypi.python.org/pypi/pyflakes>`_

  pyflakes is a great code checker that eliminates a class of possible
  errors from your code. I highly recommend using it.

  I use it with Emacs. `This page
  <http://reinout.vanrees.org/weblog/2010/05/11/pep8-pyflakes-emacs.html>`_
  covers setting up pyflakes with Emacs in a couple of different ways.

  Another way to run it is as a pre-commit hook with `check.py
  <https://github.com/jbalogh/check>`_.


Django / nose / haystack / whoosh / django-rest-framework
=========================================================

* `Django <https://www.djangoproject.com/>`_

  This software is built using Django. I tried to use Django pieces
  where possible.

* `django-nose <https://github.com/jbalogh/django-nose>`_ and
  `nose <http://readthedocs.org/docs/nose/en/latest/>`_

  Testing is done using django-nose which replaces the default Django
  test runner with nose. This makes it a one-liner to run all the
  tests and also provides some nice scaffolding for building tests and
  organizing them.

  I additionally use `nose-progressive
  <http://pypi.python.org/pypi/nose-progressive/>`_ because then the test
  output is easier to read. I highly recommend it.

* `django-haystack <http://haystacksearch.org/>`_ and
  `whoosh <https://bitbucket.org/mchaput/whoosh/wiki/Home>`_

  This runs the search system. I picked whoosh because it's a pure
  Python package and thus really easy to install and use. That makes
  richard easy for contributors to get up and running.

  You can pick a different backend by setting the appropriate
  configuration in ``settings_local.py``. See the django-haystack
  documentation for details.

* `south <http://south.aerocode.org/>`_

  South manages schema and data migrations independent on the database.

* `django-rest-framework <http://django-rest-framework.org/>`_

  django-rest-framework provides a RESTful API that can be used to retrieve
  videos programmatically and can ease importing many videos for site
  admins.


HtML / CSS / JavaScript
=======================

* `Learning HTML at MDN
  <https://developer.mozilla.org/en-US/learn/html>`_,
  `Learning CSS at MDN
  <https://developer.mozilla.org/en-US/learn/css>`_ and
  `Learning JavaScript at MDN
  <https://developer.mozilla.org/en-US/learn/javascript>`_

  These are great references for learning HTML, CSS and
  JavaScript. Highly recommended reading before you jump into the
  user-interface related code.


Video and Universal Subtitles
=============================

* `Using HTML5 audio and video
  <https://developer.mozilla.org/en/Using_HTML5_audio_and_video>`_
  covers HTML5 video tag.

* `Universal Subtitles <http://www.universalsubtitles.org/>`_ and
  `Universal Subtitles wiki <https://github.com/pculture/unisubs/wiki/>`_

  This is the subtitling system we're using. Their wiki covers embedding,
  wrapping, and the API.
