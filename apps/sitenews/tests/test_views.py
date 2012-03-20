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
from django.test import TestCase, Client
from datetime import datetime

from . import sitenews_maker


class ViewTestCase(TestCase):
    """Helper class for testing views."""

    def setUp(self):
        self.client = Client()
    
    def assert_HTTP_200(self, url):
        """Assert that the given URL returns a 200 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def assert_HTTP_404(self, url):
        """Assert that the given URL returns a 404 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def assert_used_templates(self, url, templates):
        """
        Assert that every template in ``templates`` list was rendered 
        after hitting ``url``.
        """
        response = self.client.get(url)
        for template in templates:
            self.assertTemplateUsed(response, template)


class SitenewsViewsTest(ViewTestCase):
    """Tests for the ``sitenews`` apps views."""

    def test_news(self):
        """Test the view of an individual news view."""
        news = sitenews_maker(pk=1,
                              title='Test',
                              save=True)
        url = news.get_absolute_url()

        self.assert_HTTP_200(url)
        self.assert_used_templates(url, ["sitenews/news.html"])

    def test_news_raise_404_when_does_not_exist(self):
        """Test that trying to view a non-existent news raises a 404 error."""
        news = sitenews_maker(pk=2,
                              title='Test',
                              save=False)
        url = news.get_absolute_url()

        self.assert_HTTP_404(url)

    def test_news_archive_year(self):
        """Test the view of current year's archive."""
        url = reverse('sitenews-archive-year', 
                      kwargs={'year': datetime.now().year})

        self.assert_HTTP_200(url)
        self.assert_used_templates(url, ["sitenews/news_list.html"])

    def test_news_list(self):
        """Test the list of latest news."""
        url = reverse('sitenews-list')

        self.assert_HTTP_200(url)
        self.assert_used_templates(url, ["sitenews/news_list.html"])
