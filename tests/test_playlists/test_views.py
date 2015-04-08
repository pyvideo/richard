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

from django.core.urlresolvers import reverse

from richard.playlists.models import Playlist
from . import factories
from tests import RichardTestCase, UserFactory
from tests.test_videos import factories as videos_factories


class TestPlaylistsUnauthenticated(RichardTestCase):
    def test_no_playlists_on_homepage(self):
        """No playlists link on home page if not authenticated"""
        url = reverse('home')

        resp = self.client.get(url)
        assert resp.status_code == 200
        self.assertNotContains(resp, 'My playlists')

    def test_no_playlists_on_video_page(self):
        """No playlists link on video page if not authenticated"""
        v = videos_factories.VideoFactory()
        resp = self.client.get(v.get_absolute_url())
        assert resp.status_code == 200
        self.assertNotContains(resp, 'Playlists')

    def test_playlist_list_view(self):
        """View should say the user is not authenticated"""
        resp = self.client.get(reverse('playlists-playlist-list'))
        assert resp.status_code == 200
        self.assertContains(resp, 'not logged in')


class TestPlaylistsAuthenticated(RichardTestCase):
    def setUp(self):
        # Create a user and log the user in
        self.test_user = UserFactory()
        self.client_login_user(self.test_user)
        super(RichardTestCase, self).setUp()

    def test_playlist_list_view(self):
        """Playlist view works when authenticated"""
        p = factories.PlaylistFactory(user=self.test_user)
        resp = self.client.get(reverse('playlists-playlist-list'))
        assert resp.status_code == 200
        self.assertNotContains(resp, 'not logged in')
        self.assertContains(resp, p.summary)

    def test_playlists_on_video_page(self):
        """No playlists link on video page if not authenticated"""
        v = videos_factories.VideoFactory()
        resp = self.client.get(v.get_absolute_url())
        assert resp.status_code == 200
        self.assertContains(resp, 'Playlists')

    # FIXME: Delete playlist from playlist list page

    def test_no_playlists_shows_create_link_on_video_page(self):
        # No playlists should show "Create new playlist" link
        v = videos_factories.VideoFactory()
        resp = self.client.get(v.get_absolute_url())
        assert resp.status_code == 200
        self.assertContains(resp, 'Create new playlist')

    def test_playlists_listed_on_video_page(self):
        # With a playlist should show playlist
        v = videos_factories.VideoFactory()
        p = factories.PlaylistFactory(user=self.test_user)
        resp = self.client.get(v.get_absolute_url())
        assert resp.status_code == 200
        self.assertContains(resp, 'Playlists')
        self.assertContains(resp, p.summary)

    # FIXME: Add video to playlist from video page

    # FIXME: Test playlist link on video page
