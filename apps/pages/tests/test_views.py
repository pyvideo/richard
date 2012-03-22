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

from richard.tests.utils import ViewTestCase


class PagesTest(ViewTestCase):
    """Tests for the ``pages`` apps views."""

    def test_pages(self):
        """Test a individual page."""
        for page in ['about', 'contact']:
            url = reverse('pages-page', 
                          kwargs={'page': page},)

            self.assert_HTTP_200(url)
            self.assert_used_templates(url, 
                                       templates=['pages/%s.html' % page])
