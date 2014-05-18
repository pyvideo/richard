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

import datetime
import json
from functools import partial
from imp import reload

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.encoding import smart_text

from nose.tools import eq_
from rest_framework.authtoken.models import Token

from richard.videos.tests import category, language, speaker, tag, video
from richard.videos.models import Video
from richard.videos import urls as video_urls_module


class TestNoAPI(TestCase):
    def test_api_disabled(self):
        """Test that disabled api kicks up 404"""
        with self.settings(API=False):
            reload(video_urls_module)
            vid = video(state=Video.STATE_LIVE, save=True)

            # anonymous user
            resp = self.client.get('/api/v2/video/%d/' % vid.pk,
                                   {'format': 'json'})
            eq_(resp.status_code, 404)

        reload(video_urls_module)


class TestAPIBase(TestCase):
    def setUp(self):
        """Create superuser with API key."""
        super(TestAPIBase, self).setUp()

        user = User.objects.create_superuser(
            username='api_user', email='api@example.com', password='password')
        user.save()
        token = Token.objects.create(user=user)
        token.save()

        headers = {
            'HTTP_AUTHORIZATION': 'Token {0}'.format(token.key)
        }

        self.auth_post = partial(self.client.post, **headers)
        self.auth_put = partial(self.client.put, **headers)
        self.auth_get = partial(self.client.get, **headers)


class TestCategoryAPI(TestAPIBase):
    def test_get_category_list(self):
        """Test that a category can be retrieved."""
        category(save=True)
        category(save=True)
        category(save=True)

        resp = self.client.get('/api/v2/category/',
                               {'format': 'json'})
        eq_(resp.status_code, 200)
        content = json.loads(smart_text(resp.content))
        eq_(len(content['results']), 3)

    def test_get_category(self):
        """Test that a category can be retrieved."""
        cat = category(save=True)

        resp = self.client.get('/api/v2/category/%s/' % cat.slug,
                               {'format': 'json'})
        eq_(resp.status_code, 200)
        content = json.loads(smart_text(resp.content))
        eq_(content['title'], cat.title)


class TestSpeakerAPI(TestAPIBase):
    def test_get_speakers_list(self):
        """Test that a list of speakers can be retrieved."""
        speaker(name=u'Guido van Rossum', save=True)
        speaker(name=u'Raymond Hettinger', save=True)

        resp = self.client.get('/api/v2/speaker/',
                               {'format': 'json'})
        eq_(resp.status_code, 200)
        content = json.loads(smart_text(resp.content))
        eq_(len(content['results']), 2)
        names = set([result['name'] for result in content['results']])
        eq_(names, set([u'Guido van Rossum', u'Raymond Hettinger']))


class TestAPI(TestAPIBase):
    def test_get_video(self):
        """Test that a video can be retrieved."""
        vid = video(state=Video.STATE_LIVE, save=True)

        # anonymous user
        resp = self.client.get('/api/v2/video/%d/' % vid.pk,
                               {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(smart_text(resp.content))['title'], vid.title)

        # authenticated user
        resp = self.auth_get('/api/v2/video/%d/' % vid.pk,
                             {'format': 'json'})
        eq_(resp.status_code, 200)
        eq_(json.loads(smart_text(resp.content))['title'], vid.title)

    def test_get_video_data(self):
        cat = category(title=u'Foo Title', save=True)
        vid = video(title=u'Foo Bar', category=cat, state=Video.STATE_LIVE,
                    save=True)
        t = tag(tag=u'tag', save=True)
        vid.tags = [t]
        s = speaker(name=u'Jim', save=True)
        vid.speakers = [s]

        resp = self.client.get('/api/v2/video/%d/' % vid.pk,
                               {'format': 'json'})
        eq_(resp.status_code, 200)
        content = json.loads(smart_text(resp.content))
        eq_(content['title'], vid.title)
        eq_(content['slug'], 'foo-bar')
        # This should be the category title--not api url
        eq_(content['category'], cat.title)
        # This should be the tag--not api url
        eq_(content['tags'], [t.tag])
        # This should be the speaker name--not api url
        eq_(content['speakers'], [s.name])

    def test_only_live_videos_for_anonymous_users(self):
        """Test that not authenticated users can't see draft videos."""
        vid_live = video(state=Video.STATE_LIVE, title=u'Foo', save=True)
        video(state=Video.STATE_DRAFT, title=u'Bar', save=True)

        resp = self.client.get('/api/v2/video/',
                               content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 1)
        eq_(data['results'][0]['title'], vid_live.title)

    def test_all_videos_for_admins(self):
        """Test that admins can see all videos."""
        video(state=Video.STATE_LIVE, title=u'Foo', save=True)
        video(state=Video.STATE_DRAFT, title=u'Bar', save=True)

        resp = self.auth_get('/api/v2/video/',
                             content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 2)

    def test_videos_by_tag(self):
        tag1 = tag(tag='boat', save=True)
        v1 = video(state=Video.STATE_LIVE, title=u'Foo1', save=True)
        v1.tags = [tag1]
        v1.save()
        v2 = video(state=Video.STATE_LIVE, title=u'Foo2', save=True)
        v2.tags = [tag1]
        v2.save()
        video(state=Video.STATE_LIVE, title=u'Foo3', save=True)

        resp = self.auth_get('/api/v2/video/?tag=boat',
                             content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 2)

    def test_videos_by_speaker(self):
        speaker1 = speaker(name='webber', save=True)
        v1 = video(state=Video.STATE_LIVE, title=u'Foo1', save=True)
        v1.speakers = [speaker1]
        v1.save()
        v2 = video(state=Video.STATE_LIVE, title=u'Foo2', save=True)
        v2.speakers = [speaker1]
        v2.save()
        video(state=Video.STATE_LIVE, title=u'Foo3', save=True)

        # Filter by full name.
        resp = self.auth_get('/api/v2/video/?speaker=webber',
                             content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 2)

        # Filter by partial name.
        resp = self.auth_get('/api/v2/video/?speaker=web',
                             content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 2)

    def test_videos_by_category(self):
        cat1 = category(slug="pycon-us-2014", save=True)
        cat2 = category(slug="scipy-2013", save=True)
        video(state=Video.STATE_LIVE, title=u'Foo1',
              category=cat1, save=True)
        video(state=Video.STATE_LIVE, title=u'Foo2',
              category=cat1, save=True)
        video(state=Video.STATE_LIVE, title=u'Foo3',
              category=cat2, save=True)

        resp = self.auth_get('/api/v2/video/?category=pycon-us-2014',
                             content_type='application/json')

        data = json.loads(smart_text(resp.content))
        eq_(len(data['results']), 2)

    def test_videos_by_order(self):
        video(state=Video.STATE_LIVE, title=u'FooC',
              recorded=datetime.datetime(2014, 1, 1, 10, 0),
              save=True)
        video(state=Video.STATE_LIVE, title=u'FooA',
              recorded=datetime.datetime(2013, 1, 1, 10, 0),
              save=True)
        video(state=Video.STATE_LIVE, title=u'FooB',
              recorded=datetime.datetime(2014, 2, 1, 10, 0),
              save=True)

        # Filter by title.
        resp = self.auth_get('/api/v2/video/?ordering=title',
                             content_type='application/json')
        data = json.loads(smart_text(resp.content))
        eq_([v['title'] for v in data['results']], [u'FooA', u'FooB', u'FooC'])

        # Filter by recorded.
        resp = self.auth_get('/api/v2/video/?ordering=recorded',
                             content_type='application/json')
        data = json.loads(smart_text(resp.content))
        eq_([v['title'] for v in data['results']], [u'FooA', u'FooC', u'FooB'])

        # Filter by added (reverse order).
        resp = self.auth_get('/api/v2/video/?ordering=-added',
                             content_type='application/json')
        data = json.loads(smart_text(resp.content))
        eq_([v['title'] for v in data['results']], [u'FooB', u'FooA', u'FooC'])


class TestVideoPostAPI(TestAPIBase):
    def test_post_video(self):
        """Test that authenticated user can create videos."""
        cat = category(save=True)
        lang = language(name='English', save=True)

        data = {'title': 'Creating delicious APIs for Django apps since 2010.',
                'language': lang.name,
                'category': cat.title,
                'speakers': ['Guido'],
                'tags': ['django', 'api'],
                'state': Video.STATE_LIVE}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)
        eq_(json.loads(smart_text(resp.content))['title'], data['title'])

        vid = Video.objects.get(title=data['title'])
        eq_(vid.title, data['title'])
        eq_(vid.slug, u'creating-delicious-apis-for-django-apps-since-201')
        eq_(list(vid.speakers.values_list('name', flat=True)), ['Guido'])
        eq_(sorted(vid.tags.values_list('tag', flat=True)),
            [u'api', u'django'])

    def test_post_video_no_title(self):
        """Test that no title throws an error."""
        cat = category(save=True)

        data = {'title': '',
                'category': cat.title,
                'state': Video.STATE_LIVE}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_bad_state(self):
        """Test that a bad state is rejected"""
        cat = category(save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'state': 0}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_used_slug(self):
        """Test that already used slug creates second video with new slug."""
        cat = category(save=True)
        lang = language(save=True)
        video(title='test1', slug='test1', save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'language': lang.name,
                'state': Video.STATE_DRAFT,
                'slug': 'test1'}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)

    def test_put(self):
        """Test that passing in an id, but no slug with a PUT works."""
        cat = category(save=True)
        lang = language(save=True)
        vid = video(title='test1', save=True)

        data = {'id': vid.pk,
                'title': vid.title,
                'category': cat.title,
                'language': lang.name,
                'speakers': ['Guido'],
                'tags': ['foo'],
                'state': Video.STATE_DRAFT}

        resp = self.auth_put('/api/v2/video/%d/' % vid.pk,
                             json.dumps(data),
                             content_type='application/json')
        eq_(resp.status_code, 200)

        # Get the video from the db and compare data.
        vid = Video.objects.get(pk=vid.pk)
        eq_(vid.title, u'test1')
        eq_(vid.slug, u'test1')
        eq_(list(vid.speakers.values_list('name', flat=True)), ['Guido'])
        eq_(list(vid.tags.values_list('tag', flat=True)), ['foo'])

    def test_put_fails_with_live_videos(self):
        """Test that passing in an id, but no slug with a PUT works."""
        cat = category(save=True)
        lang = language(save=True)
        vid = video(
            title='test1',
            category=cat,
            language=lang,
            state=Video.STATE_LIVE,
            save=True)

        data = {'id': vid.pk,
                'title': 'new title',
                'category': cat.title,
                'language': lang.name,
                'speakers': ['Guido'],
                'tags': ['foo'],
                'state': Video.STATE_DRAFT}

        resp = self.auth_put('/api/v2/video/%d/' % vid.pk,
                             json.dumps(data),
                             content_type='application/json')
        eq_(resp.status_code, 403)

    def test_post_with_tag_name(self):
        """Test that you can post video with url tags or real tags"""
        cat = category(save=True)
        lang = language(save=True)

        footag = u'footag'
        data = {
            'title': 'test1',
            'category': cat.title,
            'language': lang.name,
            'state': Video.STATE_DRAFT,
            'tags': [footag],
        }

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)

        # Verify the tag
        vid = Video.objects.get(title=data['title'])
        eq_(vid.tags.values_list('tag', flat=True)[0], footag)

    def test_post_with_bad_tag_string(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'state': Video.STATE_DRAFT}

        data.update({'tags': ['']})

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

        data.update({'tags': ['/api/v2/tag/1']})

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_speaker_name(self):
        """Test that you can post videos with speaker names"""
        cat = category(save=True)
        lang = language(save=True)

        fooperson = u'Carl'
        data = {
            'title': 'test1',
            'category': cat.title,
            'language': lang.name,
            'state': Video.STATE_DRAFT,
            'speakers': [fooperson],
        }

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)

        # Verify the speaker
        vid = Video.objects.get(title=data['title'])
        eq_(vid.speakers.values_list('name', flat=True)[0], fooperson)

    def test_post_with_speaker_with_extra_spaces(self):
        """Test that you can post videos with speaker names"""
        cat = category(save=True)
        lang = language(save=True)

        fooperson = u' Carl '
        data = {
            'title': 'test1',
            'category': cat.title,
            'language': lang.name,
            'state': Video.STATE_DRAFT,
            'speakers': [fooperson],
        }

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)

        # Verify the speaker
        vid = Video.objects.get(title=data['title'])
        eq_(vid.speakers.values_list('name', flat=True)[0], fooperson.strip())

    def test_post_with_bad_speaker_string(self):
        cat = category(save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'state': Video.STATE_DRAFT}

        data.update({'speakers': ['']})

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

        data.update({'speakers': ['/api/v2/speaker/1']})

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_category_title(self):
        """Test that a category title works"""
        cat = category(title='testcat', save=True)
        lang = language(name='English', save=True)

        data = {'title': 'test1',
                'language': lang.name,
                'category': cat.title,
                'state': Video.STATE_DRAFT,
                'slug': 'foo'}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 201)

    def test_post_with_no_category(self):
        """Test that lack of category is rejected"""
        data = {'title': 'test1',
                'state': Video.STATE_DRAFT}
        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_with_bad_language(self):
        """Test that a bad state is rejected"""
        cat = category(title='testcat', save=True)

        data = {'title': 'test1',
                'category': cat.title,
                'state': Video.STATE_DRAFT,
                'language': 'lolcats'}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_video_no_data(self):
        """Test that an attempt to create a video without data is rejected."""
        data = {}

        resp = self.auth_post('/api/v2/video/', json.dumps(data),
                              content_type='application/json')
        eq_(resp.status_code, 400)

    def test_post_video_not_authenticated(self):
        """Test that not authenticated users can't write."""
        cat = category(save=True)
        data = {'title': 'Creating delicious APIs since 2010.',
                'category': cat.title,
                'state': Video.STATE_LIVE}

        resp = self.client.post('/api/v2/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 401)
