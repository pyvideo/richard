# richard -- video index system
# Copyright (C) 2012 richard contributors.  See AUTHORS.
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

import json
from functools import partial

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from nose.plugins.skip import SkipTest
from nose.tools import eq_
from tastypie.models import ApiKey

from richard.videos.tests import video, speaker, category, language, tag
from richard.videos.models import Video
from richard.videos.urls import build_api_urls


urlpatterns = build_api_urls()


class TestNoAPI(TestCase):
    def test_api_disabled(self):
        """Test that disabled api kicks up 404"""
        if settings.API:
            raise SkipTest

        vid = video(state=Video.STATE_LIVE, save=True)

        # anonymous user
        resp = self.client.get('/api/v1/video/%d/' % vid.pk, {'format': 'json'})
        eq_(resp.status_code, 404)


class TestAPIBase(TestCase):
    urls = 'richard.videos.tests.test_api'

    def setUp(self):
        """Create superuser with API key."""
        user = User.objects.create_superuser(
            username='api_user', email='api@example.com', password='password')
        user.save()
        ApiKey.objects.create(user=user)

        header = 'ApiKey %s:%s' % (user.username, user.api_key.key)
        self.auth_post = partial(self.client.post, HTTP_AUTHORIZATION=header)
        self.auth_get = partial(self.client.get, HTTP_AUTHORIZATION=header)


class TestAPI(TestAPIBase):
    def test_get_video(self):
        """Test that a video can be retrieved."""
        vid = video(state=Video.STATE_LIVE, save=True)

        # anonymous user
        resp = self.client.get('/api/v1/video/%d/' % vid.pk, {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['title'], vid.title)

        # authenticated user
        resp = self.auth_get('/api/v1/video/%d/' % vid.pk, {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['title'], vid.title)

    def test_get_speaker(self):
        """Test that a speaker can be retrieved."""
        s = speaker(save=True)

        resp = self.client.get('/api/v1/speaker/%d/' % s.pk, {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['name'], s.name)

    def test_get_category(self):
        """Test that a category can be retrieved."""
        cat = category(save=True)

        resp = self.client.get('/api/v1/category/%d/' % cat.pk, {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['name'], cat.name)

    def test_only_live_videos_for_anonymous_users(self):
        """Test that not authenticated users can't see draft videos."""
        vid_live = video(state=Video.STATE_LIVE, title=u'Foo', save=True)
        video(state=Video.STATE_DRAFT, title=u'Bar', save=True)

        resp = self.client.get('/api/v1/video/',
                               content_type='application/json')

        data = json.loads(resp.content)
        eq_(len(data['objects']), 1)
        eq_(data['objects'][0]['title'], vid_live.title)

    def test_all_videos_for_admins(self):
        """Test that admins can see all videos."""
        video(state=Video.STATE_LIVE, title=u'Foo', save=True)
        video(state=Video.STATE_DRAFT, title=u'Bar', save=True)

        resp = self.auth_get('/api/v1/video/',
                             content_type='application/json')

        data = json.loads(resp.content)
        eq_(len(data['objects']), 2)


class TestVideoPostAPI(TestAPIBase):
    def test_post_video(self):
        """Test that authenticated user can create videos."""
        cat = category(save=True)

        data = {'title': 'Creating delicious APIs for Django apps since 2010.',
                'category': '/api/v1/category/%d/' % cat.pk,
                'speakers': ['Guido'],
                'tags': ['django', 'api'],
                'state': Video.STATE_LIVE}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['title'], data['title'])

        vid = Video.objects.get(title=data['title'])
        eq_(vid.title, data['title'])
        eq_(list(vid.speakers.values_list('name', flat=True)), ['Guido'])
        eq_(sorted(vid.tags.values_list('tag', flat=True)), [u'api', u'django'])

    def test_post_with_bad_state(self):
        """Test that a bad state is rejected"""
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': 0}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_used_slug(self):
        """Test that an already used slug kicks up a 400."""
        cat = category(save=True)
        video(title='test1', slug='test1', save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT,
                'slug': 'test1'}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_tag_name(self):
        """Test that you can post video with url tags or real tags"""
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        footag = u'footag'
        data.update({
                'title': 'test2',
                'tags': [footag],
                })

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})

        # Verify the tag
        vid = Video.objects.get(title=data['title'])
        eq_(vid.tags.values_list('tag', flat=True)[0], footag)

    def test_post_with_tag_url(self):
        cat = category(save=True)
        tag1 = tag(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        # Post video using /api/v1/tag/xx.
        data.update({'tags': ['/api/v1/tag/%d/' % tag1.pk]})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})

        # Verify the tag
        vid = Video.objects.get(title=data['title'])
        eq_(vid.tags.values_list('tag', flat=True)[0], tag1.tag)

    def test_post_with_bad_tag_url(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        # Post video using /api/v1/tag/xx.
        data.update({'tags': ['/api/v1/tag/50/']})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 404)

    def test_post_with_bad_tag_string(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        data.update({'tags': ['']})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_speaker_url(self):
        """Test that you can post videos with url speakers"""
        cat = category(save=True)
        speaker1 = speaker(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        # Post the video using /api/v1/speaker/xx.
        data.update({'speakers': ['/api/v1/speaker/%d/' % speaker1.pk]})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})

        # Verify the tag
        vid = Video.objects.get(title=data['title'])
        eq_(vid.speakers.values_list('name', flat=True)[0], speaker1.name)

    def test_post_with_speaker_name(self):
        """Test that you can post videos with speaker names"""
        cat = category(save=True)
        fooperson = u'Carl'
        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        data.update({
                'title': 'test2',
                'speakers': [fooperson],
                })

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        print resp.content
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})

        # Verify the speaker
        vid = Video.objects.get(title=data['title'])
        eq_(vid.speakers.values_list('name', flat=True)[0], fooperson)

    def test_post_with_bad_speaker_url(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        # Post video using /api/v1/speaker/xx.
        data.update({'speakers': ['/api/v1/speaker/50/']})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 404)

    def test_post_with_bad_speaker_string(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT}

        data.update({'speakers': ['']})

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_category_title(self):
        """Test that a category title works"""
        cat = category(title='testcat', save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'state': Video.STATE_DRAFT}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

    def test_post_with_no_category(self):
        """Test that lack of category is rejected"""
        data = {'title': 'test1',
                'state': Video.STATE_DRAFT}
        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_bad_language(self):
        """Test that a bad state is rejected"""
        cat = category(title='testcat', save=True)

        data = {'title': 'test1',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_DRAFT,
                'language': 'lolcats'}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_video_with_urls(self):
        """Test that authenticated user can create videos."""
        cat = category(save=True)
        person = speaker(save=True)
        tag1 = tag(save=True)
        tag2 = tag(save=True)
        lang = language(save=True)

        data = {'title': 'Creating delicious APIs for Django apps since 2010.',
                'category': '/api/v1/category/%d/' % cat.pk,
                'speakers': ['/api/v1/speaker/%d/' % person.pk],
                'tags': ['/api/v1/tag/%d/' % tag1.pk,
                         '/api/v1/tag/%d/' % tag2.pk],
                'language': lang.name,
                'state': Video.STATE_LIVE}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 201)

        # Get the created video
        resp = self.auth_get(resp['Location'], {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(resp.content)['title'], data['title'])

        # Verify the data
        vid = Video.objects.get(title=data['title'])
        eq_(vid.title, data['title'])
        eq_(list(vid.speakers.values_list('name', flat=True)), [person.name])
        eq_(sorted(vid.tags.values_list('tag', flat=True)),
            sorted([tag1.tag, tag2.tag]))
        eq_(vid.language.name, lang.name)

    def test_post_video_no_data(self):
        """Test that an attempt to create a video without data is rejected."""
        data = {}

        resp = self.auth_post('/api/v1/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 404)

    def test_post_video_not_authenticated(self):
        """Test that not authenticated users can't write."""
        cat = category(save=True)
        data = {'title': 'Creating delicious APIs for Django apps since 2010.',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_LIVE}

        resp = self.client.post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 401)

