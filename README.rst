========
 README
========

richard is a video index site.

It's pretty basic at the moment. I'm adding functionality as I need it for
`<http://pyvideo.org>`_. If you're looking at this or using it at this
stage, then you're either a friend of mine or you're intrigued by the
future possibilities.

My priorities:

1. Maximize ease of finding the video you're looking for.
2. Minimize site upkeep and maintenance---it's an index and it should pretty
   much run itself.
3. Make it easy for others to help maintain the index data.
4. Minimize work for adding new video.

Features richard currently has:

* index of videos
* site news
* support for HTML5 video

Things I'm thinking about in the future:

* feeds: every listing should have a feed view of it
* Universal Subtitles support
* on-site support for adding a conference of videos and individual
  videos


Project details
===============

Code:
    https://github.com/willkg/richard

Issue tracker:
    https://github.com/willkg/richard/issues

Documentation:
    Documentation is in the ``docs/`` directory including docs for
    installing, upgrading, deploying, contributing, ...

    Also at: http://richard.readthedocs.org/

IRC channel:
    ``richard`` on ``irc.freenode.net``


Want to help?
=============

Is this project useful to you now? Do you think it might be useful to you
in the future? Does it sound like something you want to be involved in?

I'd love to have help! Here are things I need help with:

* documentation work

  * verifying correctness of the existing documentation
  * fixing errors in the documentation
  * fixing TODO items in the documentation

* styling work

  * make the default site look better

* code work

  * correct egregious errors which are probably due to misunderstandings of
    how Django and other components work
  * working on issues in the issue tracker
  * fixing TODO items in the code

* testing work

  * write tests---there's test infrastructure, but no tests, yet which
    is totally lame
  * test richard---there are no tests, so it's likely there are issues
  * test richard on browsers other than Firefox nightly---I use Firefox
    nightly and haven't looked at richard on anything else
  * test richard on mobile devices---does it work well in tablets? does
    it work well on phones? what hardware does it not work well on?

* community work

  * do you know other groups looking for video index software? tell them
    about richard.

* project infrastructure work

  * is there infrastructure missing in this project that would make it
    easier for you to collaborate? if so, what?


Tests
=====

Run::

    ./manage.py test
