=============
 Conventions
=============

Python code
===========

* PEP-8: http://www.python.org/dev/peps/pep-0008/
* PEP-257: http://www.python.org/dev/peps/pep-0257/
* Use pyflakes. Srsly.

pep8 covers Python code conventions. pep257 covers Python docstring
conventions.

Minor caveats:

* We use Sphinx, so do function definitions like they do:
  `<http://packages.python.org/an_example_pypi_project/sphinx.html#function-definitions>`_.
* Don't kill yourself over 80-character lines, but it is important.
* If you're flummoxed by the conventions, just send me the patch and
  as long as it functionally works, I can do a cleanup pass in a
  later commit.


HTML/Jinja2 templates
=====================

.. todo:: html/jinja2 template conventions


CSS
===

.. todo:: css conventions


JavaScript
==========

.. todo:: javascript conventions


Git
===

I encourage good commit messages in a form that works well with
git's various commands. Something like
`<http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_. except
that I don't care about verb tense or capitalization and if the
commit message is tied to a bug report, the bug report number should
be the first thing in the first line. Here's the tbaggery example
with some adjustments::

    475. short summary (50 chars or less)

    More detailed explanatory text, if necessary.  Wrap it to about
    72 characters or so.  In some contexts, the first line is
    treated as the subject of an email and the rest of the text as
    the body.  The blank line separating the summary from the body
    is critical (unless you omit the body entirely); tools like
    rebase can get confused if you run the two together.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too

    - Typically a hyphen or asterisk is used for the bullet,
      preceded by a single space, with blank lines in between, but
      conventions vary here

    - Use a hanging indent

Why? Here's the reasons:

* 50 characters or less works well with the various git commands
  that show only the summary line and also on github.
* Having the bug number as the first thing makes it easy to see
  which commits covered which bugs without parsing the commit
  message. We do that a lot ("When did the fix for bug xyz land?").
* Wrapping the subsequent paragraphs allows them to show up nicely
  in git output as well as on github.

Why not the other things? Here's the reasons:

* Capitalization or non-capitalization for a phrase doesn't affect
  the output of git commands or my ability to quickly parse a
  summary.
* Ditto for verb tense.
* I'm all for ditching convention baggage for things that don't matter.

