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

from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_

from sitenews.tests import notification


class RichardViewsTest(TestCase):
    """Tests for the project's views."""

    def test_home(self):
        url = reverse('home')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')

    def test_notifications_on_home(self):
        """Test that notifications are displayed on the homepage."""
        n1 = notification(text=u'1, 2, 3 - test', save=True)
        n2 = notification(text=u'Just a test.', save=True)

        resp = self.client.get(reverse('home'))
        assert n1.text in resp.content
        assert n2.text in resp.content

    def test_stats(self):
        """Test the statistics page."""
        url = reverse('stats')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
