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

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'richard.playlists.views',

    # playlists
    url(r'^playlist/$',
        'playlist_list', name='playlists-playlist-list'),
    url(r'playlist/delete/?$',
        'playlist_delete', name='playlists-playlist-delete'),
    url(r'playlist/remove-video/?$',
        'playlist_remove_video', name='playlists-playlist-remove-video'),
    url(r'playlist/(?P<playlist_id>[0-9]+)/?$',
        'playlist', name='playlists-playlist'),
)
