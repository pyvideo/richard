.. _api-chapter:

=====
 API
=====

richard comes with an REST API built with `django-rest-framework
<http://django-rest-framework.org/>`_.


.. contents::
   :local:


Enabling the API
================

The API is disabled by default. To enable the API, add this to your
`richard/settings_local.py` file::

    API = True


API tokens and authenticating
=============================

.. Note::

   The API keys used in richard v 0.1 are different than the API
   tokens used in richard v 0.2 and later. If you were using richard
   v0.1, you'll need to create new API tokens when you upgrade to
   v0.2.

Anonymous users have:

* read-only access to video data

Authenticated users have:

* read/create/update access to video data

To authenticate, you need a valid API token. To get one, you need to:

1. log into the richard admin
2. click on `Tokens` in the `Authtoken` section
3. click on `Add token` in the upper right
4. select the user you want to add a key for in the drop down
5. click on `Save` in bottom right hand corner

After doing that, your API token will be generated and will be in the
`Key` field.

Use the `Authorization` HTTP header to authenticate. The value is your
API token.

For example, using curl::

    $ curl --dump-header - \
        -H "Content-Type: application/json" \
        -H "Authentication: Token abd984049d938e8909ff" \
        -X POST 'http://example.com/api/v2/video/' \
        -d '
    {
        "tag": "foo"
        ...
    }'


Obviously, that data doesn't work, but the header structure is correct.


API
===

Category
--------

``GET /api/v2/category/``
    Lists categories.

    Example::

      $ curl -X GET 'http://example.com/api/v2/category/'

``GET /api/v2/category/<CATEGORY_SLUG>/``
    Lists information about that category.

    Example::

      $ curl -X GET 'http://example.com/api/v2/category/pycon-2011/'


Speaker
-------

``GET /api/v2/speaker/``
    Lists speakers.

    Example::

      $ curl -X GET 'http://example.com/api/v2/speaker/'


Videos
------

``GET /api/v2/video/``
    Lists all the videos on the site. This is paginated. The
    pagination fields are at the top level and titled `next` and
    `previous`.

    Example::

      $ curl -X GET 'http://example.com/api/v2/video/'

``GET /api/v2/video/<VIDEO_ID>/``
    Returns information for that specific video id.

    Example::

      $ curl -X GET 'http://example.com/api/v2/video/2/'

``GET /api/v2/video/?speaker=FOO``
    Returns videos with speaker FOO. It only handles one speaker, but
    it uses `icontains` on the speaker field which will do
    case-insensitive substring matches.

    Example::

      $ curl -X GET 'http://example.com/api/v2/video/?speaker=asheesh'

``GET /api/v2/video/?tag=FOO``
    Returns videos with tag FOO. It only takes one tag and does an
    exact match.

    Example::

      $ curl -X GET 'http://example.com/api/v2/video/?tag=django'

``POST /api/v2/video/``
    Creates a new video.

``PUT /api/v2/video/<VIDEO_ID>/``
    Updates an existing video.

    .. Note::

       You can only update videos in DRAFT mode. If it's live, you
       will get an error.


Fields for creating/updating videos:

    **category** --- Required.
        The title of the category.

        The category must exist on the site. If it doesn't exist, the
        API will waggle its finger at you. (Oops!)

        Example: ``"category": "PyCon 2012"``

    **title** --- Required.
        The title of the video.

        Example: ``"title": "My dog has fleas"``

    **language** --- Required.
        Name of the language that the video is primarily in. For example,
        if the speaker is speaking English, then the video is in English.

        The language must exist on the site. If it doesn't exist, the API
        will waggle its finger at you.

        Example: ``"language": "English"``

    **state** --- Required.
        Possible values:

        * 1 - live
        * 2 - draft

        Example: ``"state": 1``

    **summary** --- Required.
        Short summary of the video formatted in Markdown. Should be no
        more than a single paragraph of a few sentences.

    **description**
        Longer description of the video in Markdown. Outlines, linked
        timecodes, etc would go here.

    **tags**
        List of tags.

        If you pass in tags and they don't exist, the API will create
        them for you. If they do exist, the API will associate the
        video with the existing tag objects. (Yay!)

        Example: ``"tags": ["web", "django", "beard"]``

        .. Note::

            If you're updating a video, you have to pass in the
            complete set of tags every time. If you pass no tags,
            it'll remove them assuming that you meant to remove all
            the tags.

    **speakers**
        List of speaker names

        If you pass in speaker names and they don't exist, the API
        will create them for you. If they do exist, the API will
        associate the video with the existing speaker objects. (Yay!)

        Example: ``"speakers": ["Carl Karsten", "Chris Webber"]``

        .. Note::

           If you're updating a video, you have to pass in the
           complete set of speakers every time. If you pass no
           speakers, it'll remove them assuming that you meant to
           remove all the speakers.

    **source_url**
        The url where the video resides. For example, if this video
        were hosted on YouTube, then you'd provide the YouTube url for
        it.

    FIXME - Finish documenting fields. See code for the rest of the
    fields.


Here's minimal JSON example for a video::

    {
      "category": "Test Category",
      "title": "Test video title",
      "language": "English",
      "state": 1
    }


Here's a slightly longer one::

    {
      "category": "Test Category",
      "title": "Test video title",
      "language": "English",
      "state": 1,
      "speakers": ["Jimmy Discotheque"],
      "tags": ["test", "bestever"],
      "summary": "Jimmy tests things out.",
      "description": "Tests\nAnd more tests."
    }
