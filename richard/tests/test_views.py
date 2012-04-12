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
from sitenews.tests import notification


class RichardViewsTest(ViewTestCase):
    """Tests for the project's views."""

    def test_home(self):
        url = reverse('home')

        self.assert_HTTP_200(url)
        self.assert_used_templates(url, 
                                   templates=['home.html'])

    def test_notifications_on_home(self):
        """Test that notifications are displayed on the homepage."""
        notification(text=u'1, 2, 3 - test', save=True)
        notification(text=u'Just a test.', save=True)

        url = reverse('home')
        self.assert_contains(url, text='1, 2, 3 - test')
        self.assert_contains(url, text='Just a test.')
