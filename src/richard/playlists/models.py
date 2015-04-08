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
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from richard.videos.models import Video


@python_2_unicode_compatible
class Playlist(models.Model):
    user = models.ForeignKey(User, help_text='User that owns this playlist')
    summary = models.CharField(
        max_length=100, help_text='Summary of the playlist')
    description = models.TextField(
        blank=True, default=u'',
        help_text='Long description of the playlist (in markdown).')
    data = models.CommaSeparatedIntegerField(
        max_length=255, blank=True, default=u'',
        help_text='Comma-separated list of video ids for this playlist.')

    updated = models.DateTimeField(
        auto_now=True, help_text='Last time this playlist was updated.')

    def _get_data(self):
        """Return videos in this playlist

        :returns: list of ints

        """
        return [int(videoid) for videoid in self.data.split(',') if videoid]

    def _set_data(self, data):
        """Sets data

        :arg data: list of int video ids

        """
        self.data = ','.join(str(videoid) for videoid in data)

    def has_video(self, videoid):
        """Checks to see if videoid is in the playlist

        :arg videoid: int

        """
        return videoid in self._get_data()

    def append_video(self, video):
        if isinstance(video, Video):
            video = video.id
        if self.has_video(video):
            return
        video = str(video)
        data = self._get_data()
        data.append(video)
        self._set_data(data)
        self.save()

    def remove_video(self, video):
        if isinstance(video, Video):
            video = video.id
        data = self._get_data()
        data.remove(video)
        self._set_data(data)
        self.save()

    def set_videos(self, videos):
        if isinstance(videos[0], Video):
            videos = [video.id for video in videos]
        self._set_data(videos)
        self.save()

    def video_list(self):
        """Returns list of Video instances"""
        if not self.data:
            return []
        return [Video.objects.get(pk=int(videoid))
                for videoid in self.data.split(',')]

    def video_count(self):
        """Returns number of videos in playlist"""
        return len(self._get_data())

    def __str__(self):
        return '%d: %s' % (self.id, self.summary)

    def __repr__(self):
        return '<Playlist %d: %s>' % (
            self.id, self.summary.encode('ascii', 'ignore'))

    class Meta(object):
        ordering = ['summary']

    @models.permalink
    def get_absolute_url(self):
        return ('playlists-playlist', (self.pk,))
