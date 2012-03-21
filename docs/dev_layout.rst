================
 Project layout
================

When you do a ``git clone ...`` of richard, you end up with a
directory tree like this::

   richard
   |- docs/          -- documentation
   |- requirements/  -- requirements files for pip
   |- richard/       -- richard django project
   \- apps/
      |- pages/      -- code for "about", "contac", etc pages
      |- sitenews/   -- code for sitenews
      \- videos/     -- code for videos and search


Here's what's there:

**richard/docs/**

    Documentation for the project build wtih Sphinx and formatted in
    restructuredtext.

**richard/requirements/**

    ``.txt`` files that you use with pip to install richard's
    requirements.

**richard/richard/**

    This is the "Django project" part of the project.

**richard/apps/**

    This is where the "Django apps" go. There are a few:

    **pages**

        Like django.contrib.flatpages except that nothing is in the
        database---it's all done with templates.

    **sitenews**

        Bare-bones "blog" for your site allowing you to specify site
        news like changes, new conferences added, etc.

    **videos**

        This app does most of the work and manages speakers,
        categories (conferences, user groups, etc), videos and search.
