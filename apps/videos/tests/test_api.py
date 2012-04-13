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

from django.test import TestCase
from nose.tools import eq_

from . import video, speaker, category
from videos.models import Video


class TestApi(TestCase):

    def test_get_video(self):
        """Test that a video can be retrieved."""
        vid = video(state=Video.STATE_LIVE, save=True)

        resp = self.client.get('/api/v1/video/%d/' % vid.pk, {'format': 'json'})
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
