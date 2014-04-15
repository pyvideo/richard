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

import sys
from functools import partial

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from nose.tools import eq_
from rest_framework.authtoken.models import Token
if sys.version_info < (3, 0):
    from steve import richardapi

    from richard.videos.models import Category, Video
    from richard.videos.tests import category, language


    class TestSteveAndAPI(LiveServerTestCase):
        # LiveServerTestCase launches richard on setup and shuts it down
        # on teardown--that's per test.
        #
        # URL is self.live_server_url
        @property
        def api_url(self):
            return self.live_server_url + '/api/v2/'

        def setUp(self):
            super(TestSteveAndAPI, self).setUp()
            """Create superuser with API key."""
            self.user = User.objects.create_superuser(
                username='api_user', email='api@example.com', password='password')
            self.user.save()
            self.token = Token.objects.create(user=self.user)
            self.token.save()

        def test_get_categories(self):
            cat = category(save=True)
            cats = richardapi.get_all_categories(self.api_url)
            eq_(len(cats), 1)
            cats[0]['title'] = cat.title

        def test_get_category(self):
            cat = category(save=True)
            cat_from_api = richardapi.get_category(self.api_url, cat.title)
            eq_(cat_from_api['title'], cat.title)

        def test_create_and_update_video(self):
            cat = category(save=True)
            lang = language(name=u'English', save=True)

            ret = richardapi.create_video(
                self.api_url,
                auth_token=self.token.key,
                video_data={
                    'title': 'Test video',
                    'language': lang.name,
                    'category': cat.title,
                    'state': 2,  # Has to be draft so update works
                    'speakers': ['Jimmy'],
                    'tags': ['foo'],
                })

            video = Video.objects.get(title='Test video')

            eq_(video.title, ret['title'])
            eq_(video.state, ret['state'])
            eq_(video.id, ret['id'])

            ret['title'] = 'Video Test'
            ret = richardapi.update_video(
                self.api_url,
                auth_token=self.token.key,
                video_id=ret['id'],
                video_data=ret
            )

            video = Video.objects.get(title='Video Test')
            eq_(video.title, ret['title'])
