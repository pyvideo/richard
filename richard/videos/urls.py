# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, url

from richard.videos.feeds import (
    CategoryFeed, CategoryVideosFeed, SpeakerVideosFeed,
    NewPostedVideoFeed)
from richard.videos.views import (
    CategoryListAPI, CategoryRetrieveAPI, VideoListCreateAPI,
    VideoRetrieveUpdateAPI, SpeakerListAPI)


urlpatterns = patterns(
    'richard.videos.views',

    # categories
    url(r'^category/?$',
        'category_list', name='videos-category-list'),
    url(r'^category/(?P<category_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/?$',
        'category', name='videos-category'),
    url(r'^category/rss/?$',
        CategoryFeed(), name='videos-category-feed'),
    url(r'^category/(?P<category_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/rss/?$',
        CategoryVideosFeed(), name='videos-category-videos-feed'),
    url(r'^category/(?P<category_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/files/?$',
        'category_files', name='videos-category-files'),

    # speakers
    url(r'^speaker/$',
        'speaker_list', name='videos-speaker-list'),
    url(r'^speaker/(?P<speaker_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/?$',
        'speaker', name='videos-speaker'),
    url(r'^speaker/(?P<speaker_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/rss/?$',
        SpeakerVideosFeed(), name='videos-speaker-feed'),

    # videos
    url(r'^video/(?P<video_id>[0-9]+)(?:/(?P<slug>[\w-]*))?/?$',
        'video', name='videos-video'),
    url(r'^video/rss/?$', NewPostedVideoFeed(), name='videos-new-feed'),

    # search
    url(r'^search/?$',
        'search', name='videos-search'),
    url(r'^search/xml/?$',
        'opensearch', name='videos-opensearch'),
    url(r'^search/suggestions/$',
        'opensearch_suggestions', name='videos-opensearch-suggestions'),

    # faux api for carl
    url(r'^api/1.0/videos/urlforsource$',
        'apiurlforsource', name='videos-api-urlforsource'),
)


def build_api_urls():
    """Builds the API-related urls"""
    return patterns(
        '',

        # v1 was done with tastypie. It's been dumped for v1 which was
        # redone with Django-REST-Framework.
        url(r'^api/v2/category/?$', CategoryListAPI.as_view()),
        url(r'^api/v2/category/(?P<slug>[\w-]*)/?$',
            CategoryRetrieveAPI.as_view()),

        url(r'^api/v2/speaker/?$', SpeakerListAPI.as_view()),

        url(r'^api/v2/video/?$', VideoListCreateAPI.as_view()),
        url(r'^api/v2/video/(?P<pk>\d+)/?$',
            VideoRetrieveUpdateAPI.as_view(), name='videos-api-view'),

    )


# API is disabled by default. To enable it, add ``API = True`` to your
# settings.py file.
if settings.API:
    urlpatterns += build_api_urls()
