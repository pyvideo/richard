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

from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_

from ..test_notifications import notification
from ..test_videos import factories as video_factories


class RichardViewsTest(TestCase):
    """Tests for the project's views."""

    def test_home(self):
        url = reverse('home')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home_branded.html')

    def test_notifications_on_home(self):
        """Test that notifications are displayed on the homepage."""
        n1 = notification(text=u'1, 2, 3 - test', save=True)
        n2 = notification(text=u'Just a test.', save=True)

        resp = self.client.get(reverse('home'))
        self.assertContains(resp, n1.text)
        self.assertContains(resp, n2.text)

    def test_stats(self):
        """Test the statistics page."""
        url = reverse('stats')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)

    def test_sitemap(self):
        """Test for the sitemap.xml"""
        video_factories.CategoryFactory()
        video_factories.SpeakerFactory()
        video_factories.VideoFactory()

        resp = self.client.get('/sitemap.xml')
        eq_(resp.status_code, 200)

    def test_404(self):
        """Test for 404 page"""
        resp = self.client.get('/carlspants')
        eq_(resp.status_code, 404)
