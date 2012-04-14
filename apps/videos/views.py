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
import json

from django.contrib.sites.models import Site
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from haystack.query import SearchQuerySet


from videos import models


def category_list(request):
    category_kinds = models.CategoryKind.objects.all()

    ret = render(
        request, 'videos/category_list.html',
        {'kinds': category_kinds})
    return ret


def category(request, category_id, slug):
    obj = get_object_or_404(models.Category, pk=category_id)

    ret = render(
        request, 'videos/category.html',
        {'category': obj})
    return ret


def speaker_list(request):
    # TODO: Should cache this--no need to look it up every time.
    qs = models.Speaker.objects.values_list('name', flat=True)
    chars = list(set(sname[0].lower() for sname in qs))
    chars.sort()

    c = request.GET.get('character', 'a')

    # make sure that there are speakers in the DB
    if chars:
        if len(c) != 1 or c not in chars:
            c = chars[0]

    speakers = models.Speaker.objects.filter(name__istartswith=c)

    ret = render(
        request, 'videos/speaker_list.html',
        {'chars': chars,
         'active_char': c,
         'speakers': speakers})
    return ret


def speaker(request, speaker_id, slug=None):
    obj = get_object_or_404(models.Speaker, pk=speaker_id)

    ret = render(
        request, 'videos/speaker.html',
        {'speaker': obj})
    return ret


def video(request, video_id, slug):
    obj = get_object_or_404(models.Video, pk=video_id)

    meta = [
        ('keywords', ",".join([t.tag for t in obj.tags.all()]))
        ]
    if obj.summary:
        meta.append(('description', 
                     bleach.clean(obj.summary, tags=[], strip=True)))

    ret = render(
        request, 'videos/video.html',
        {'meta': meta,
         'v': obj})
    return ret


def opensearch(request):
    ret = render(
        request, 'videos/opensearch.xml',
        {'site': Site.objects.get_current()},
        content_type='application/opensearchdescription+xml')
    return ret


def opensearch_autocomplete(request):
    """Return autocompletions for a search query.
    
    Implements the OpenSearch suggestions extension.
    """
    query = request.GET.get('q', '')
    matches = SearchQuerySet().filter(title_auto=query)
    result = [query, [r.object.title for r in matches]]

    return JSONResponse(json.dumps(result))


# TODO: Move this elsewhere

class JSONResponse(HttpResponse):
     def __init__(self, content):
         super(JSONResponse, self).__init__(
             content, mimetype='application/json')


def apiurlforsource(request):
    host_url = request.GET.get('host_url')
    if not host_url:
        raise Http404

    obj = get_object_or_404(models.Video, source_url=host_url)
    return JSONResponse('{"source_url": "http://pyvideo.org%s"}' % obj.get_absolute_url())
