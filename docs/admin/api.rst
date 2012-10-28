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
`richard/settings_local.py` file::

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

richard uses Tastypie to implement the API.

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

For example::

    $ curl -XGET 'http://example.com/api/v1/'

lists the endpoints for what can be retrieved through the API.

The API only returns JSON because I think it makes it easier to use.

GET requests that return long lists of things return a page of that
list. There's a `meta` section in the response that tells you which
page you requested and how to get the next page.


Authenticating
==============

There are two groups of users: site admin and everyone else. Only site
admin need to authenticate.

Tastypie lets you authenticate via querystring parameters as well as
HTTP header.  We'll cover authenticating by querystring parameters
here. You need to provide two key/value pairs:

* ``username`` - your richard site admin username
* ``api_key`` - the api key for your account

For example, using curl::

    $ curl --dump-header - -H "Content-Type: application/json" \
        -X POST --data '{"tag": "foo"}' \
        'http://example.com/api/v1/tag/?username=USERNAME&api_key=KEY'

.. seealso::

   http://django-tastypie.readthedocs.org/en/latest/authentication_authorization.html#apikeyauthentication
     API Key authentication docs


API
===


Videos
------

``GET /api/v1/video/``

    Lists all the videos on the site.

``GET /api/v1/video/<VIDEO_ID>/``

    Returns information for that specific video id.

``GET /api/v1/video/?speaker=FOO``

    Returns videos with speaker FOO. It only handles one speaker, but
    it uses icontains which will do case-insensitive substring
    matches.

``GET /api/v1/video/?tag=FOO``

    Returns videos with tag FOO. It only takes one tag and does an
    exact match.

``POST /api/v1/video/``

    Creates a new video.

``POST /api/v1/video/<VIDEO_ID>/``

    Updates an existing video.


Intersting things to keep in mind when creating new videos or updating
existing ones:

* **category**

  Required.

  The title of the category.

  The category must already exist. If it doesn't exist, the API will
  waggle its finger at you. (Oops!)

  Example::

      "category": "PyCon 2012"

  .. Note::

     This is the category *title* not the category *name*.

* **state**

  Required.

  * 1 - live
  * 2 - draft

  Example::

      "state": 1

* **title**

  The title of the video.

  Example::

      "title": "My dog has fleas"

  .. Note::

     Unlike summary and description, this is just a string and not in
     HTML.

* **summary** and **description**

  The summary and description should be in valid HTML.

  Example::

      "summary": "<p>This is a summary</p>"

  and::

      "description": "<p>This is a description.</p>\n<p>La la la!</p>"

* **tags**

  List of tags.

  If you pass in tags and they don't exist, the API will create them
  for you. If they do exist, the API will associate the video with the
  existing tag objects. (Yay!)

  Example::

      "tags": ["web", "django", "beard"]

  .. Note::

     If you're updating a video, you have to pass in the complete set
     of tags every time. If you pass no tags, it'll remove them
     assuming that you meant to remove all the tags.

* **speakers**

  List of speaker names

  If you pass in speaker names and they don't exist, the API will
  create them for you. If they do exist, the API will associate the
  video with the existing speaker objects. (Yay!)

  Example::

      "speakers": ["Carl Karsten", "Chris Webber"]

  .. Note::

     If you're updating a video, you have to pass in the complete set
     of speakers every time. If you pass no speakers, it'll remove
     them assuming that you meant to remove all the speakers.

* **language**

  The name of the language. This comes from the languages table.

  If the language doesn't exist, the API will waggle its finger at
  you. (Oops!)

  Example::

      "language": "English"


Here's an minimal JSON example for a video::

    {
      "category": "Test Category",
      "state": 1,
      "title": "Test video title"
    }

Here's a slightly longer one::

    {
      "category": "Test Category",
      "state": 1,
      "title": "Test video title",
      "speakers": ["Jimmy Discotheque"],
      "tags": ["test", "bestever"],
      "summary": "<p>Jimmy tests things out.</p>",
      "description": "<p>Tests</p>\n<p>And more tests</p>",
      "language": "English"
    }

Everything else should be self-explanatory. See the schema::

    curl http://example.com/api/v1/video/schema/

replacing `example.com` with your server and port.


Category
--------

``/api/v1/category/``

    Lists categories.


``/api/v1/category/<CATEGORY_ID>/``

    Lists information about that category.


More?
=====

It's definitely worth looking at the `Tastypie documentation
<http://django-tastypie.readthedocs.org/en/latest/interacting.html>`_
for more examples and such.
