===========
 Resources
===========

This chapter is a list of resources and notes that I thought would be
helpful to new people who want to contribute to this software. There's
also some design decisions and code conventions in here, too.

.. contents::


Project scaffolding
===================

* `playdoh <http://playdoh.readthedocs.org/en/latest/index.html>`_ and
  `kitsune <http://kitsune.readthedocs.org/en/latest/>`_

  Kitsune is the name of the project I work on at Mozilla. Playdoh is
  the name of the Django web application template that most Mozilla
  webdev projects are built on top of.

  I use both for inspiration for project scaffolding.


Settings
--------

`<https://docs.djangoproject.com/en/dev/topics/settings/#django.conf.settings.configure>`_
talks about settings, but doesn't cover separating settings into
multiple settings files.

richard uses ``settings_local.py`` for locally overriding settings
defaults. We do the same thing for some of our projects at
Mozilla. Also, James Bennett talks about using ``local_settings.py`` in
"Practical Django Projects" [PDP2009] which is essentially the same,
but with a slightly different name. I like ``settings_local.py``
better than ``local_settings.py`` since then all my settings files
get listed next to each other when sorted alphabetically.

.. [PDP2009] Practical Django Projects, by James Bennett

For tests, richard uses ``settings_test.py`` which allows us to
override settings explicitly for the test environment. We do this at
Mozilla and it makes things a lot easier.


Requirements / environments / deployment
----------------------------------------

* `virtualenv <http://pypi.python.org/pypi/virtualenv>`_ and
  `pip <http://pypi.python.org/pypi/pip>`_

  richard uses virtualenv and pip to build the environment for richard
  to run.

  Requirements are listed in ``requirements/`` in multiple files. The
  base requirements are in ``requirements/base.txt`` and other
  use-oriented requirements files include that and then add additional
  requirements. This makes it easier to specify different kinds of
  environments like development and deployment.

  pip reads the requirements files, downloads requirements, and installs
  them into the virtual environment.

  It works pretty well except when PyPI is down.

  We may revisit this later if this becomes an annoying problem.


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


Django / nose / jinja2 / haystack / whoosh
==========================================

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
  output is easier to read.

* `jingo <https://github.com/jbalogh/jingo>`_ and
  `jinja2 <http://jinja.pocoo.org/>`_

  The Django templates are nice, but I prefer Jinja2 templates. The
  Jinja2 docs cover `differences between Django and Jinja2 templating
  engines <http://jinja.pocoo.org/docs/switching/#django>`_, though
  Django 1.4 adds ``elif``, so that's no longer a difference.

* `django-haystack <http://haystacksearch.org/>`_ and
  `whoosh <https://bitbucket.org/mchaput/whoosh/wiki/Home>`_

  This runs the search system. I picked whoosh because it's a pure Python
  package and thus really easy to install and use.

  You can pick something different and change ``settings_local.py`` with
  the appropriate configuration.
  

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
