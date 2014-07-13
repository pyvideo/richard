================
 Project layout
================

When you do a ``git clone ...`` of richard, you end up with a
directory tree like this::

   richard
   |- docs/          -- documentation
   |-src/
     \- richard/       -- richard django project
         |- base/       -- base code shared by the other apps
         |- config/     -- settings and configuration
         |- pages/      -- code for "about", "contac", etc pages
         |- sampledata/ -- code for loading sampledata from apps
         |- sitenews/   -- code for sitenews
         \- videos/     -- code for videos and search


Here's what's there:

**richard/docs/**

    Documentation for the project build wtih Sphinx and formatted in
    restructuredtext.

**src/richard/**

    This is the "Django project" part of the project and where the
    "Django apps" go. There are a few:

    **base**

        This is where shared code for all the apps go as well as code
        central to the Django project. Middleware, context processors,
        base templates, static assets, etc.

    **config**

        This is where the settings and wsgi files live.

    **pages**

        Like django.contrib.flatpages except that nothing is in the
        database---it's all done with templates.

    **sampledata**

        Small utility app that will load sample data from other apps
        for development.

    **sitenews**

        Bare-bones "blog" for your site allowing you to specify site
        news like changes, new conferences added, etc.

    **videos**

        This app does most of the work and manages speakers,
        categories (conferences, user groups, etc), videos and search.
