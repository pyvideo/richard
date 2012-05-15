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

from django.conf import settings
from django.db.models import Count
from django.shortcuts import render


from videos.models import CategoryKind, Video, Category, Speaker, Tag
from sitenews.models import SiteNews


def home(request):
    category_list = CategoryKind.objects.all()
    news_list = SiteNews.objects.all()[:5]
    video_count = Video.objects.live().count()

    ret = render(
        request, 'home.html',
        {'title': settings.SITE_TITLE,
         'kinds': category_list,
         'news': news_list,
         'video_count': video_count})
    return ret


def stats(request):
    """List statistics about the collection.

    E.g. number of videos, top 5 categories.
    """

    # Retrieve objects of model `m`, ordered by the number of videos they have
    most_videos = lambda m: (m.objects.filter(video__state=Video.STATE_LIVE)
                                      .annotate(count=Count('video'))
                                      .order_by('-count'))

    video_count = Video.objects.live().count()

    category_count = Category.objects.count()
    category_top5 = most_videos(Category)[:5]

    speaker_count = Speaker.objects.count()
    speaker_top5 = most_videos(Speaker)[:5]

    tag_count = Tag.objects.count()
    tag_top5 = most_videos(Tag)[:5]

    ret = render(
        request, 'stats.html',
        {'video_count': video_count,
         'category_count': category_count,
         'category_top5': category_top5,
         'speaker_count': speaker_count,
         'speaker_top5': speaker_top5,
         'tag_count': tag_count,
         'tag_top5': tag_top5})
    return ret
