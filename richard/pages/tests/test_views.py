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
from django.test.utils import override_settings
from nose.tools import eq_


class TestPages(TestCase):
    """Tests for the ``pages`` apps views."""

    def test_about_page(self):
        """Test about page"""
        url = reverse('pages-page', kwargs={'page': 'about'},)

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/about.html')

    def test_nonexistent_page_throws_404(self):
        """Test that a page without matching template returns 404"""
        url = reverse('pages-page', kwargs={'page': 'doesnotexist'})

        resp = self.client.get(url)
        eq_(resp.status_code, 404)

    @override_settings(PAGES=[])
    def test_page_without_template_throws_404(self):
        """Test that a registered page without template returns 404"""
        url = reverse('pages-page', kwargs={'page': 'about'},)

        resp = self.client.get(url)
        eq_(resp.status_code, 404)
