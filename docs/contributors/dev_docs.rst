===============
 Documentation
===============


.. contents::
   :local:


In the code
===========

Documentation in the code is really helpful. Please add comments where
you think it's necessary.

We like to use docstrings for classes, methods and functions. They
should be in reStructuredText format. Something along these lines,
though most of our docstrings aren't as formal or complete::

    def foo(arg1, arg2):
        """Foo does something interesting

        :arg arg1: Controls whether or not to bar
        :arg arg2: Name of the baz to use

        :raises ValueError: If arg2 is not a valid baz.

        :returns: A bat.
        """

The purpose in-code documentation is three-fold:

1. to clarify complex code so it's easier to discern what it's doing
2. to make it clear why the code is doing what it's doing
3. to document any issues the code might have


The administrator's guide and contributor's guide
=================================================

These two guides live in ``docs/``.

We use `Sphinx <http://sphinx.pocoo.org/>`_ to structure and build our
documentation.

To build the documentation, do::

    $ cd docs/
    $ make html

The docs are available in HTML and PDF forms at
`<http://richard.readthedocs.org/>`_. Whenever something is committed
and pushed to the master branch, GitHub pings ReadTheDocs and the docs
that are there are rebuilt.
