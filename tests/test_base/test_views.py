# richard -- video index system
# Copyright (C) 2012, 2013, 2014, 2015 richard contributors.  See AUTHORS.
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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from richard.base.models import Profile

from tests import RichardTestCase, UserFactory
from tests.test_notifications import factories as notification_factories
from tests.test_videos import factories as video_factories


class RichardViewsTest(TestCase):
    """Tests for the project's views."""

    def test_home(self):
        url = reverse('home')

        resp = self.client.get(url)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'home_branded.html')

    def test_notifications_on_home(self):
        """Test that notifications are displayed on the homepage."""
        n1 = notification_factories.NotificationFactory(text=u'1, 2, 3 - test')
        n2 = notification_factories.NotificationFactory(text=u'Just a test.')

        resp = self.client.get(reverse('home'))
        self.assertContains(resp, n1.text)
        self.assertContains(resp, n2.text)

    def test_stats(self):
        """Test the statistics page."""
        url = reverse('stats')

        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_sitemap(self):
        """Test for the sitemap.xml"""
        video_factories.CategoryFactory()
        video_factories.SpeakerFactory()
        video_factories.VideoFactory()

        resp = self.client.get('/sitemap.xml')
        assert resp.status_code == 200

    def test_404(self):
        """Test for 404 page"""
        resp = self.client.get('/carlspants')
        assert resp.status_code == 404


class NewUserTest(RichardTestCase):
    def test_new_user_page_redirects_to_home(self):
        """Anonymous users get redirected to home"""
        resp = self.client.get(reverse('new_user'), follow=True)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'base.html')

    def test_new_user_page(self):
        """New users get sent to new_user page"""
        # Create a new user with no profile
        jane = UserFactory(profile=None)
        # Try to use the profile attribute. If there is no profile,
        # then it kicks up a DoesNotExist error. We want that.
        try:
            jane.profile
            assert False, 'Profile exists, but should not'
        except Profile.DoesNotExist:
            pass

        self.client_login_user(jane)
        resp = self.client.get(reverse('new_user'))
        assert resp.status_code == 200
        self.assertContains(resp, 'using Persona')

        jane = User.objects.get(username=jane.username)
        assert jane.profile is not None
