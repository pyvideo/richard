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

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from richard.base.utils import smart_int
from richard.playlists import models


def playlist_delete(request):
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse('playlists-playlist-list'))
    playlist_id = smart_int(request.POST.get('playlistid', None))

    if playlist_id is None:
        return HttpResponseRedirect(reverse('playlists-playlist-list'))

    try:
        playlist = models.Playlist.objects.get(
            pk=playlist_id,
            user=request.user
        )
    except models.Playlist.DoesNotExist:
        return HttpResponseRedirect(reverse('playlists-playlist-list'))
    
    if not 'forrealz' in request.POST:
        ret = render(
            request, 'playlists/playlist_delete_confirm.html',
            {'playlist': playlist})
        return ret
    
    models.Playlist.objects.filter(pk=playlist_id, user=request.user).delete()
    # FIXME: Add a confirmation message.
    return HttpResponseRedirect(reverse('playlists-playlist-list'))


def playlist_list(request):
    if not request.user.is_authenticated():
        ret = render(
            request, 'playlists/playlist_notauthed.html')
        return ret
    
    if request.method == 'POST':
        name = request.POST.get('playlistname', '')
        if name:
            playlist = models.Playlist.objects.create(
                user=request.user,
                summary=name
            )
            playlist.save()
        return HttpResponseRedirect(reverse('playlists-playlist-list'))
            
    playlists = models.Playlist.objects.filter(user=request.user)

    ret = render(
        request, 'playlists/playlist_list.html',
        {'playlists': playlists})
    return ret


def playlist(request, playlist_id):
    obj = get_object_or_404(models.Playlist, pk=playlist_id)

    ret = render(
        request, 'playlists/playlist.html',
        {'playlist': obj})
    return ret


def playlist_remove_video(request):
    playlist_id = smart_int(request.POST.get('playlist_id', None))
    if playlist_id is None:
        print('playlist is none')
        return HttpResponseRedirect(reverse('playlists-playlist-list'))

    try:
        playlist = models.Playlist.objects.get(
            pk=playlist_id,
            user=request.user
        )
    except models.Playlist.DoesNotExist:
        return HttpResponseRedirect(reverse('playlists-playlist-list'))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('playlists-playlist-list'))

    video_id = smart_int(request.POST.get('video_id', None))
    if video_id is None:
        return HttpResponseRedirect(reverse('playlists-playlist', args=(playlist_id,)))

    playlist.remove_video(video_id)
    print('removed')
    # FIXME: Message to user
    return HttpResponseRedirect(reverse('playlists-playlist', args=(playlist_id,)))
