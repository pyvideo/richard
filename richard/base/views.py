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

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import is_safe_url

from richard.base.models import Profile
from richard.suggestions.models import Suggestion
from richard.videos.models import Video, Category, Speaker, Tag


def home(request):
    latest_categories = Category.objects.order_by('-added')[:10]
    latest_videos = Video.objects.live().order_by('-added')[:10]

    video_count = Video.objects.live().count()

    ret = render(
        request, 'home_branded.html',
        {'title': settings.SITE_TITLE,
         'latest_categories': latest_categories,
         'latest_videos': latest_videos,
         'video_count': video_count})
    return ret


def login_failure(request):
    return render(request, 'login_failure.html')


def new_user(request):
    if request.user.is_anonymous():
        # This is the AnonymousUser and they shouldn't be here
        # so push them home.
        return HttpResponseRedirect(reverse('home'))

    try:
        # If they have a profile, then this doesn't throw an error
        # and we can let them see the new user view again, but it's
        # not particularly interesting.
        request.user.profile
    except Profile.DoesNotExist:
        # They aren't anonymous and don't have a profile, so create
        # a profile for them.
        #
        # We could do more with this, but we're not at the moment.
        Profile.objects.create(user=request.user)

    next_url = request.GET.get('next', reverse('home'))
    if not is_safe_url(next_url):
        next_url = reverse('home')

    return render(request, 'new_user.html', {
        'next_url': next_url,
    })


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

    open_states = (Suggestion.STATE_NEW, Suggestion.STATE_IN_PROGRESS)
    suggestions = (Suggestion.objects.filter(
        state__in=open_states, is_reviewed=True).order_by('-state'))

    ret = render(
        request, 'stats.html',
        {'video_count': video_count,
         'category_count': category_count,
         'category_top5': category_top5,
         'speaker_count': speaker_count,
         'speaker_top5': speaker_top5,
         'tag_count': tag_count,
         'tag_top5': tag_top5,
         'suggestions': suggestions})
    return ret
