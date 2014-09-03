========
 Readme
========

richard is software for running a video index site.

We developed it with the following priorities:

1. Make it easy for users to find videos they're looking for. This
   includes making it easy to search for videos and browse
   videos. Additionally, the site has feeds allowing users to
   subscribe to things that interest them and thus get notified when
   there are new things

2. Minimize the work required to maintain the site---it's an index and
   it should pretty much run itself.

3. Minimize the server requirements---it's an index of videos, so the
   less that's running on the server, the easier it is for someone to
   put together their own video index site.


Features richard currently has:

* videos, speakers, tags and categories
* site notifications: one-liners that show up on every page of the
  site for critical updates
* feeds: category feed, speaker feed
* HTML5 video and embedded video support and Amara subtitles
* site search backed by django-haystack
* API: HTTP GET access for everyone and HTTP PUT/DELETE for admin
* decent documentation at http://richard.rtfd.org/

We're actively working on fixing bugs, adding new features,
refactoring bad design decisions, making it more flexible, and
improving the documentation. Check out the `issue tracker
<http://github.com/pyvideo/richard/issues>`_ for some of the things
we're working on.


Versions
========

There is no released version of richard, yet. If you look at the
commit history, you'll see we're moving along with functionality. When
we hit a critical mass of important bits, we'll do a round of polish
and release a 0.1. Until then, if you want to use it, you should use
it from git master.

And join us on the IRC channel!


Project details
===============

:Code:          https://github.com/pyvideo/richard
:Issue tracker: https://github.com/pyvideo/richard/issues
:Documentation: http://richard.rtfd.org/
:IRC channel:   ``#richard`` on ``irc.freenode.net``
:License:       AGPLv3


Documentation is also in the ``docs/`` directory. This includes docs for
installing, upgrading, deploying, contributing, ...

Our unit tests are run by Travis CI every time we commit to the
master branch.

.. image:: https://secure.travis-ci.org/pyvideo/richard.png?branch=master
   :target: http://travis-ci.org/pyvideo/richard


Who's using richard?
====================

Known sites using richard:

* http://pyvideo.org/

If you're using richard and want to be added to this site, let us know!


Want to help?
=============

Is this project useful to you now? Do you think it might be useful to
you in the future? Does it sound like something you want to be
involved in?

I'd love to have help! We have a special `Contributor's Guide
<http://richard.readthedocs.org/en/latest/contributors/dev_contribute.html>`_
in the richard manual that covers how to get richard set up for
hacking on it, the kinds of things we need help on, and all the sorts
of things you'd want to know about the project.


Install, Upgrade, Configuration
===============================

See the `richard documentation <http://richard.rtfd.org/>`_.
