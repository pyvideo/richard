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
from django.test import TestCase

from . import factories
from tests.test_videos.factories import VideoFactory


class TestPlaylistModel(TestCase):
    def test_operations(self):
        user = User.objects.create_user(
            username='joe', email='joe@example.com', password='ou812')
        user.save()

        vid1 = VideoFactory()
        vid2 = VideoFactory()
        vid3 = VideoFactory()

        playlist = factories.PlaylistFactory(user=user, summary='test')
        assert playlist.data == ''
        assert playlist.video_list() == []
        assert playlist.video_count() == 0

        playlist.append_video(vid1)
        assert playlist.data == ('%d' % vid1.id)
        assert playlist.video_list() == [vid1]
        assert playlist.video_count() == 1

        playlist.append_video(vid2)
        assert playlist.data == ('%d,%d' % (vid1.id, vid2.id))
        assert playlist.video_list() == [vid1, vid2]
        assert playlist.video_count() == 2

        playlist.append_video(vid3)
        assert playlist.data == ('%d,%d,%d' % (vid1.id, vid2.id, vid3.id))
        assert playlist.video_list() == [vid1, vid2, vid3]
        assert playlist.video_count() == 3

        playlist.remove_video(vid2)
        assert playlist.data == ('%d,%d' % (vid1.id, vid3.id))
        assert playlist.video_list() == [vid1, vid3]
        assert playlist.video_count() == 2

        playlist.set_videos([vid3, vid1])
        assert playlist.data == ('%d,%d' % (vid3.id, vid1.id))
        assert playlist.video_list() == [vid3, vid1]
        assert playlist.video_count() == 2
