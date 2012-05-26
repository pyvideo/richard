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

from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_

from richard.sitenews.tests import sitenews


class TestSitenews(TestCase):
    """Tests for the ``sitenews`` apps views."""

    def test_news_list(self):
        """Test the list of latest news."""
        sitenews(save=True)
        url = reverse('sitenews-list')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sitenews/news_list.html')

    def test_news(self):
        """Test the view of a news."""
        news = sitenews(save=True)
        url = news.get_absolute_url()

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sitenews/news.html')

    def test_news_raise_404_when_does_not_exist(self):
        """
        Test that trying to view a non-existent news raises returns 
        an HTTP 404 error.
        """
        url = reverse('sitenews-news', args=(1234, 'random-slug'))

        resp = self.client.get(url)
        eq_(resp.status_code, 404)

    def test_news_archive_year(self):
        """Test the view of current year's archive."""
        sitenews(save=True)
        url = reverse('sitenews-archive-year', 
                      kwargs={'year': datetime.now().year})

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sitenews/news_list.html')
