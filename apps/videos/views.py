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

import bleach


from django.shortcuts import get_object_or_404
import jingo


from richard import utils
from videos import models


def category_list(request):
    category_kinds = models.CategoryKind.objects.all()

    ret = jingo.render(
        request, 'videos/category_list.html',
        {'title': utils.title(u'Categories'),
         'kinds': category_kinds})
    return ret


def category(request, category_id, slug):
    obj = get_object_or_404(models.Category, pk=category_id)

    ret = jingo.render(
        request, 'videos/category.html',
        {'title': utils.title(obj.title),
         'category': obj})
    return ret


def speaker_list(request):
    c = request.GET.get('character', 'a')
    try:
        if c not in 'abcdefghijklmnopqrstuvwxyz':
            c = 'a'
    except TypeError:
        c = 'a'

    # TODO: build list of "empty characters"
    speakers = models.Speaker.objects.filter(name__istartswith=c)

    ret = jingo.render(
        request, 'videos/speaker_list.html',
        {'title': utils.title(u'Speakers'),
         'active_c': c,
         'speakers': speakers})
    return ret


def speaker(request, speaker_id, slug=None):
    obj = get_object_or_404(models.Speaker, pk=speaker_id)

    ret = jingo.render(
        request, 'videos/speaker.html',
        {'title': utils.title(obj.name),
         'speaker': obj})
    return ret


def video(request, video_id, slug):
    obj = get_object_or_404(models.Video, pk=video_id)

    meta = [
        ('keywords', ",".join([t.tag for t in obj.tags.all()]))
        ]
    if obj.summary:
        meta.append(('description', 
                     bleach.clean(obj.summary, tags=[], strip=True)))

    ret = jingo.render(
        request, 'videos/video.html',
        {'title': utils.title(obj.title),
         'meta': meta,
         'v': obj})
    return ret
