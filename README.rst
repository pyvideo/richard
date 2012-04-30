========
 README
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
* site news: let's you keep your users up to speed with site changes
* site notifications: one-liners that show up on every page of the
  site for critical updates
* feeds: site news feed, category feed, speaker feed
* HTML5 video and embedded video support
* site search backed by django-haystack
* API: HTTP GET access for everyone and HTTP PUT/DELETE for admin
* decent documentation at http://richard.readthedocs.org/

We're actively working on fixing bugs, adding new features,
refactoring bad design decisions, making it more flexible, and
improving the documentation. Check out the `issue tracker
<http://github.com/willkg/richard/issues>`_ for some of the things
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

Code:
    https://github.com/willkg/richard

    Our unit tests are run by Travis CI every time we commit to the
    master branch.

    .. image:: https://secure.travis-ci.org/willkg/richard.png?branch=master
       :target: http://travis-ci.org/willkg/richard

Issue tracker:
    https://github.com/willkg/richard/issues

Documentation:
    Documentation is in the ``docs/`` directory including docs for
    installing, upgrading, deploying, contributing, ...

    Most recent docs are at: http://richard.readthedocs.org/

IRC channel:
    ``#richard`` on ``irc.freenode.net``


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

See the `richard documentation <http://richard.readthedocs.org/>`_.
