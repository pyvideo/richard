==================
 Making it faster
==================

django-staticgenerator
======================

If you're using richard in a predominantly read-only way, then you should
take a look at using `django-staticgenerator
<https://github.com/luckythetourist/staticgenerator>`_. It takes pages
generated and stores them on disk. Then you can have your web-server serve
the file on disk instead of kicking off the django application which is way
faster.

I'm using Apache with mod_wsgi, so I used the instructions `here
<http://nemesisdesign.net/blog/coding/setup-django-staticgenerator-apache-mod_wsgi/>`_.
