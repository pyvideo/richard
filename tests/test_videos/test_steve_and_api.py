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

from django.conf import settings
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from nose.tools import eq_
from rest_framework.authtoken.models import Token
if sys.version_info < (3, 0):
    from steve import richardapi

    from richard.videos.models import Video
    from . import factories


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
            cat = factories.CategoryFactory()
            cats = richardapi.get_all_categories(self.api_url)
            eq_(len(cats), 1)
            cats[0]['title'] = cat.title

        def test_get_category(self):
            cat = factories.CategoryFactory()
            cat_from_api = richardapi.get_category(self.api_url, cat.title)
            eq_(cat_from_api['title'], cat.title)

        def test_create_and_get_video(self):
            cat = factories.CategoryFactory()
            lang = factories.LanguageFactory(name=u'English 1')

            ret = richardapi.create_video(
                self.api_url,
                auth_token=self.token.key,
                video_data={
                    'title': 'Test video create and get',
                    'language': lang.name,
                    'category': cat.title,
                    'state': richardapi.STATE_DRAFT,
                    'speakers': ['Jimmy'],
                    'tags': ['foo'],
                })

            vid = richardapi.get_video(
                self.api_url,
                auth_token=self.token.key,
                video_id=ret['id'])
            eq_(vid['id'], ret['id'])
            eq_(vid['title'], ret['title'])

        def test_create_and_update_video(self):
            cat = factories.CategoryFactory()
            lang = factories.LanguageFactory(name=u'English 2')

            ret = richardapi.create_video(
                self.api_url,
                auth_token=self.token.key,
                video_data={
                    'title': 'Test video create and update',
                    'language': lang.name,
                    'category': cat.title,
                    'state': richardapi.STATE_DRAFT,
                    'speakers': ['Jimmy'],
                    'tags': ['foo'],
                })

            video = Video.objects.get(title='Test video create and update')

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
