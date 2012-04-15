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

from django.contrib.auth.models import User
from django.test import TestCase
from nose.tools import eq_
from tastypie.models import ApiKey

from . import video, speaker, category
from videos.models import Video


class TestApi(TestCase):

    def setUp(self):
        """Create superuser with API key."""
        user = User.objects.create_superuser(
            username='api_user', email='api@example.com', password='password')
        user.save()
        ApiKey.objects.create(user=user)

        header = 'ApiKey %s:%s' % (user.username, user.api_key.key)
        self.auth_post = partial(self.client.post, HTTP_AUTHORIZATION=header)
        self.auth_get = partial(self.client.get, HTTP_AUTHORIZATION=header)

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

    def test_read_only(self):
        """Test that not authenticated users can't write."""
        cat = category(save=True)
        data = {'title': 'Creating delicious APIs for Django apps since 2010.',
                'category': '/api/v1/category/%d/' % cat.pk,
                'state': Video.STATE_LIVE}

        resp = self.client.post('/api/v1/video/', json.dumps(data),
                                content_type='application/json')
        eq_(resp.status_code, 401)
