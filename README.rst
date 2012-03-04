========
 README
========

Richard is a video index site.

It's pretty basic at the moment. I'm adding functionality as I need it for
`<http://pyvideo.org>`_. If you're looking at this or using it at this
stage, then you're either a friend of mine or you're intrigued by the
future possibilities.

My priorities:

1. Maximize ease of finding the video you're looking for.
2. Minimize site upkeep and maintenance---it's an index and it should pretty
   much run itself.
3. Minimize work for adding new video.

Things I'd like to implement at some point in the future:

* search: terms search for quickly finding things
* navigation: from a given video, easily navigate to related videos on a
  variety of axes like speaker, conference, keywords, ...
* feeds: every listing should have a feed view of it
* Universal Subtitles
* Popcorn.js
* democratizing video metadata upkeep: this is foo-foo speak for making it
  easy for anyone to make the metadata better


Project details
===============

Code:
    https://github.com/willkg/richard

Issue tracker:
    https://github.com/willkg/richard/issues

Documentation:
    Documentation is in the ``docs/`` directory including docs for
    installing, upgrading, deploying, contributing, ...


Tests
=====

Run::

    ./manage.py test
