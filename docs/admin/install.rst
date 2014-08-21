====================
 Installing richard
====================

FIXME: This needs to be written. For now, you can look at the
:ref:`hacking-chapter`, use postgresql and skip the things that are
development-environment specific.

Settings
------------

richard relies extensively on environment settings which **will not work with
Apache/mod_wsgi setups**.

For configuration purposes, the following table maps the 'richard'
environment variables to their Django setting:

======================================= =========================== ============================================== ===========================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ===========================================
DJANGO_DATABASES                        DATABASES                   See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  secret-value                                   raises error
RICHARD_API                             API                         True                                           False
RICHARD_SITE_URL                        SITE_URL                    http://127.0.0.1:8000                          http://127.0.0.1:8000
======================================= =========================== ============================================== ===========================================
