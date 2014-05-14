# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
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

from django.db.models import Count
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from haystack.query import SearchQuerySet
from rest_framework import generics
from rest_framework import permissions

from richard.videos import models


def split_year(title):
    """Returns (title base, year)

    Some categories have a year at the end. This detects that
    and returns a split.

    Example:
    >>> split_year('Foo')
    ('Foo', None)
    >>> split_year('PyCon 2013')
    ('PyCon', 2013)

    """
    try:
        title = title.strip()
        return title[:-4].strip(), int(title[-4:])
    except (IndexError, ValueError):
        return title, None


def category_list(request):
    categories = models.Category.objects.order_by('title')

    # category title -> list of categories
    cats = {}
    for cat in categories:
        title, year = split_year(cat.title)
        cat.title_year = year
        cats.setdefault(title, []).append(cat)

    # convert to dicts
    cats = [{'title': key, 'cats': val} for key, val in cats.items()]
    ret = render(request, 'videos/category_list.html', {
        'cats_by_group': cats
    })
    return ret


def category(request, category_id, slug):
    obj = get_object_or_404(models.Category, pk=category_id)

    if request.user.is_staff:
        videos = obj.video_set.all()
    else:
        videos = obj.video_set.live()

    videos = videos.select_related('category').prefetch_related('speakers')

    ret = render(
        request, 'videos/category.html',
        {'view': 'videos',
         'category': obj,
         'videos': videos})
    return ret


def category_files(request, category_id, slug):
    obj = get_object_or_404(models.Category, pk=category_id)

    videos = obj.video_set.live().prefetch_related('speakers')

    ret = render(
        request, 'videos/category.html',
        {'view': 'files',
         'category': obj,
         'videos': videos})
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

    speakers = (models.Speaker.objects.filter(name__istartswith=c)
                                      .annotate(video_count=Count('video')))

    ret = render(
        request, 'videos/speaker_list.html',
        {'chars': chars,
         'active_char': c,
         'speakers': speakers})
    return ret


def speaker(request, speaker_id, slug=None):
    obj = get_object_or_404(models.Speaker, pk=speaker_id)

    if request.user.is_staff:
        videos = obj.video_set.all()
    else:
        videos = obj.video_set.live()

    videos = videos.select_related('category').prefetch_related('speakers')

    ret = render(
        request, 'videos/speaker.html',
        {'speaker': obj,
         'videos': videos})
    return ret


def video(request, video_id, slug):
    obj = get_object_or_404(models.Video, pk=video_id)

    meta = [
        ('keywords', ",".join([t.tag for t in obj.tags.all()]))
        ]
    if obj.summary:
        meta.append(('description',
                     bleach.clean(obj.summary, tags=[], strip=True)))

    # Figure out how we're going to embed the video.
    # This is used by JavaScript code to seek to a specific video position.

    if obj.source_url and 'youtube' in obj.source_url:
        # Universal Subtitles is hardcoded for YouTube videos
        embed_type = 'unisubs'
    elif obj.embed:
        embed_type = 'custom'
    else:
        embed_type = 'html5'

    embed = obj.embed
    html5_formats = obj.get_html5_formats()
    if obj.is_youtube():
        video_url = obj.source_url
    elif html5_formats:
        video_url = html5_formats[0]['url']
    else:
        video_url = None

    use_amara = settings.AMARA_SUPPORT

    ret = render(request, 'videos/video.html', {
        'meta': meta,
        'v': obj,
        'use_amara': use_amara,
        'video_url': video_url,
        'embed': embed,
        'embed_type': embed_type,
        'html5_formats': html5_formats
    })
    return ret


def search(request):
    q = request.GET.get('q', '')
    facet_counts = {}
    if q:
        cat_filter = request.GET.get('category')

        qs = SearchQuerySet()
        qs = qs.filter(content=q)
        qs = qs.filter_or(speakers__startswith=q.lower())

        if cat_filter:
            # TODO: This doesn't work quite right. It should filter
            # out anything that's not *exactly* cat_filter but it's
            # not. Could be a problem here or with the indexing. The
            # haystack docs are mysterious.
            qs = qs.filter_and(category__exact=cat_filter)

        # TODO: Whoosh doesn't handle faceting, so we have to do it
        # manually. Fix this so it detects whether the haystack backend
        # supports facets and if so, uses the backend and not the db.
        cat_counts = {}
        for mem in qs:
            cat_counts[mem.category] = cat_counts.get(mem.category, 0) + 1

        facet_counts['category'] = sorted(
            cat_counts.items(), key=lambda pair: pair[1], reverse=True)

        page = Paginator(qs, 25)
        p = request.GET.get('p', '1')
        try:
            p = max(1, int(p))
        except ValueError:
            p = 1

        try:
            page = page.page(p)
        except EmptyPage:
            page = page.page(1)

    else:
        page = None

    if q:
        title = u'Search: {query}'.format(query=q)
    else:
        title = u'Search'

    get_params = request.GET.copy()
    if 'category' in get_params:
        get_params.pop('category')
    base_url = request.path + '?' + get_params.urlencode()

    return render(
        request,
        'videos/search.html', {
            'query': q,
            'base_url': base_url,
            'title': title,
            'facet_counts': facet_counts,
            'page': page
        })


def opensearch(request):
    """Return opensearch description document."""
    ret = render(
        request, 'videos/opensearch.xml',
        {'site': Site.objects.get_current()},
        content_type='application/opensearchdescription+xml')
    return ret


def opensearch_suggestions(request):
    """Return suggestions for a search query.

    Implements the OpenSearch suggestions extension.
    """
    if not settings.OPENSEARCH_ENABLE_SUGGESTIONS:
        raise Http404

    query = request.GET.get('q', '')
    sqs = (SearchQuerySet().filter(title_auto=query)
                           .values_list('title_auto', flat=True))
    result = [query, list(sqs)]

    return JSONResponse(json.dumps(result))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only admins get write access to resources"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # We restrict PUT to only videos in DRAFT mode. Once it's
        # live, you can only change metadata via the web interface.
        if request.method == 'PUT' and obj.state == models.Video.STATE_LIVE:
            return False

        return True


class CategoryListAPI(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = models.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    paginate_by = 50


class CategoryRetrieveAPI(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = models.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class SpeakerListAPI(generics.ListAPIView):
    queryset = models.Speaker.objects.all()
    serializer_class = models.SpeakerSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginate_by = 50


class VideoListCreateAPI(generics.ListCreateAPIView):
    serializer_class = models.VideoSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = models.Video.objects.all()
        else:
            queryset = models.Video.objects.live().all()

        speaker = self.request.QUERY_PARAMS.get('speaker', None)
        if speaker is not None:
            queryset = queryset.filter(
                speakers__in=(
                    models.Speaker.objects
                    .filter(name__icontains=speaker)
                    .values_list('pk', flat=True)))

        tag = self.request.QUERY_PARAMS.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(
                tags__in=(
                    models.Tag.objects
                    .filter(tag__icontains=tag)
                    .values_list('pk', flat=True)))

        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = queryset.filter(
                category__slug=category)

        return queryset


class VideoRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = models.Video.objects.all()
    serializer_class = models.VideoSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = models.Video.objects.all()
        else:
            queryset = models.Video.objects.live().all()

        return queryset


# TODO: Move this elsewhere

class JSONResponse(HttpResponse):
    def __init__(self, content):
        super(JSONResponse, self).__init__(
            content, content_type='application/json')


def apiurlforsource(request):
    host_url = request.GET.get('host_url')
    if not host_url:
        raise Http404

    obj = get_object_or_404(models.Video, source_url=host_url)
    return JSONResponse('{"source_url": "http://pyvideo.org%s"}' %
                        obj.get_absolute_url())
