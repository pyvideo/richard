.. _api-chapter:

=====
 API
=====

richard comes with an REST API built with `tastypie
<http://django-tastypie.readthedocs.org/>`_.


.. contents::
   :local:


Enabling the API
================

The API is disabled by default. To enable the API, add this to your
`settings.py` file::

    API = True


API keys
========

Anonymous users have read-only access to all the data except videos
that are in DRAFT status.

Site admin can do that as well as with an API key:

* see videos in DRAFT status
* delete items
* create items
* update items

richard uses `Tastypie
<http://django-tastypie.readthedocs.org/en/latest/index.html>`_ to
implement the API.

To get an API key, you need to:

1. log into the richard admin
2. click on `Api keys` in the `Tastypie` section
3. click on `Add api key` in the upper right
4. select the user you want to add a key for in the drop down
5. (completely not obvious step) click on `Save and continue editing`
   button

After doing that, your API key will be generated and will be in the
box marked `Key`.


Using the API
=============

Tastypie is super helpful in that the data it returns tells you about
the API and how to navigate it.

Example::

    $ curl -XGET 'http://example.com/api/v1/'

Lists the endpoints for what can be retrieved through the API.

The API only returns JSON because I think it makes it easier to use.

GET request that involve lists of things return a page of
data. There's a `meta` section in the response that tells you how to
get the next page.


Authenticating
==============

There are two groups of users: site admin and everyone else. Only site
admin need to authenticate.

Tastypie lets you authenticate via querystring parameters as well as
`HTTP header`_.  We'll cover authenticating by querystring parameters
here. You need to provide two key/value pairs:

* ``username`` - your richard site admin username
* ``api_key`` - the api key for your account

.. _HTTP header: http://django-tastypie.readthedocs.org/en/latest/authentication_authorization.html#apikeyauthentication


API
===


Videos
------

``/api/v1/video/``

    Lists all the videos on the site.

GET ``/api/v1/video/<VIDEO_ID>/``

    Returns information for that specific video id.

POST ``/api/v1/video/<VIDEO_ID>/``

    Updates an existing video.

POST ``/api/v1/video/``

    Creates a new video.


Intersting things to keep in mind when creating new videos or updating
existing ones:

* `state` - 1 for live, 2 for draft

* `tags` - list of tags or tag API resource urls

  e.g.: ``["web", "django", "beard"]`` or
  ``["/api/v1/tag/4/", "/api/v1/tag/19/"]``

  If you pass in tags and they don't exist, the API will create them
  for you. If they do exist, the API will associate the video with the
  existing tag objects. (Yay!)

* `speakers` - list of speaker names or tag API resource urls

  e.g.: ``["Carl Karsten", "Chris Webber"]`` or
  ``["/api/v1/speaker/4/", "/api/v1/speaker/19/"]``

  If you pass in speaker names and they don't exist, the API will
  create them for you. If they do exist, the API will associate the
  video with the existing speaker objects. (Yay!)

* `language` - the name of the language

  e.g.: ``"English"``

  If the language doesn't exist, the API will waggle its finger at
  you. (Oops!)

* `category` - the title of the category or category API resource url

  e.g.: ``"PyCon 2012"`` or ``"/api/v1/category/22/"``

  The category must already exist. If it doesn't exist, the API will
  waggle its finger at you. (Oops!)

* `summary` and `description` - the summary and description should be
  in valid HTML

* `title` - just a string -- NOT in HTML

Everything else should be self-explanatory. See the schema::

    curl http://localhost:8000/api/v1/video/schema/


Category
--------

``/api/v1/category/``

    Lists categories.


``/api/v1/category/<CATEGORY_ID>/``

    Lists information about that category.


Speakers
--------

``/api/v1/speaker/``

    Lists speakers.

``/api/v1/speaker/<SPEAKER_ID>/``

    Lists information about that speaker.


Tags
----

``/api/v1/tag/``

    Lists tags.

``/api/v1/tag/<TAG_ID>/``

    Lists information about that tag.


Long winded example
===================

We're going to use curl on the command line here, but you can use
anything that can do RESTful sorts of things.

Let's say I want to see the endpoints for a richard instance running
on my laptop::

    $ curl --dump-header - -X GET 'http://localhost:8000/api/v1/'

    HTTP/1.0 200 OK
    Date: Thu, 14 Jun 2012 13:59:13 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Content-Type: application/json; charset=utf-8

    {
        "category": {
            "list_endpoint": "/api/v1/category/",
            "schema": "/api/v1/category/schema/"
        },
        "speaker": {
            "list_endpoint": "/api/v1/speaker/",
            "schema": "/api/v1/speaker/schema/"
        },
        "tag": {
            "list_endpoint": "/api/v1/tag/",
            "schema": "/api/v1/tag/schema/"
        },
        "video": {
            "list_endpoint": "/api/v1/video/",
            "schema": "/api/v1/video/schema/"
        }
    }


That returns JSON data that shows me the various endpoints that this
API supports---all of those endpoints are listed above.

Let's find all the videos where I'm the speaker.

I don't know my speaker id, so let's get a list of all the speakers::

    $ curl --dump-header - -X GET 'http://localhost:8000/api/v1/speaker/'

    HTTP/1.0 200 OK
    Date: Thu, 14 Jun 2012 16:02:43 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Vary: Cookie
    Content-Type: application/json; charset=utf-8

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 187
        },
        "objects": [
            ... skipping a bunch ...
            {
                "id": "42",
                "name": "Me",
                "resource_uri": "/api/v1/speaker/42/",
                "slug": "me",
                "videos": [
                    "/api/v1/video/2/"
                ]
            },
            ... skipping a bunch ...
        ]
    }


There I am---speaker 42! Plus it shows the video I did.

Let's look at that video::

    $ curl -X GET 'http://localhost:8000/api/v1/video/2/'

    HTTP/1.0 200 OK
    Date: Thu, 14 Jun 2012 16:03:30 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Vary: Cookie
    Content-Type: application/json; charset=utf-8

    {
        "added": "2012-05-25T19:38:39.986217",
        "category": "/api/v1/category/2/",
        "id": "2",
        "resource_uri": "/api/v1/video/2/",
        "slug": "me-myself-and-i",
        "speakers": [
            "/api/v1/speaker/42/"
        ],
        "state": 1,
        "summary": "<p>All about me.</p>",
        "tags": [],
        "title": "Me, Myself and I",
        ... skipping ...
    }


There's a bunch of information there. One thing I notice is that this
video has no tags.

Well, this video is clearly about egotism so we should add that as a
tag. I'm a site admin, so I can update data on the site with the API.

Let's create the tag first::

    $ curl --dump-header - -H "Content-Type: application/json" \
    -X POST --data '{"tag": "foo"}' \
    'http://localhost:8000/api/v1/tag/?username=USERNAME&api_key=KEY'

    HTTP/1.0 201 CREATED
    Date: Thu, 14 Jun 2012 15:17:10 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Content-Type: text/html; charset=utf-8
    Location: http://localhost:8000/api/v1/tag/11/


The `Location` is the uri for your new tag. Let's see what's there::

    $ curl --dump-header - -X GET 'http://localhost:8000/api/v1/tag/11/'

    HTTP/1.0 200 OK
    Date: Thu, 14 Jun 2012 16:04:18 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Vary: Cookie
    Content-Type: application/json; charset=utf-8

    {"id": "11", "resource_uri": "/api/v1/tag/11/", "tag": "bar", "videos": []}

There aren't any videos associated with that tag. So let's add that
tag to video 2. First we get all the data for video 2 and modify the
tags field.

Then we push that resulting data to the site::

    $ curl --dump-header - -H "Content-Type: application/json" -X PUT --data \
    '... bunch of json here... "tags": ["egotist"], ... more json ...' \
    'http://localhost:8000/api/v1/video/2/?username=USERNAME&api_key=KEY

    HTTP/1.0 201 CREATED
    Date: Thu, 14 Jun 2012 15:54:10 GMT
    Server: WSGIServer/0.1 Python/2.7.3rc2
    Content-Type: text/html; charset=utf-8
    Location: http://localhost:8000/api/v1/video/2/

.. Note::

   Actually, the Tastypie docs suggest it should kick back an HTTP
   204, so I'm not sure why I get this back.

Now the video has the additional tag.

.. Note::

   You have to post all the data for a video even stuff you're not
   updating because otherwise the API will change fields to default
   values.


That's it for this quick example.

It's definitely worth looking at the `Tastypie documentation
<http://django-tastypie.readthedocs.org/en/latest/interacting.html>`_
for more examples and such.
