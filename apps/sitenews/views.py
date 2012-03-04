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

from django.shortcuts import get_object_or_404
import jingo

from sitenews import models


def get_years():
    return [d.year for d in models.SiteNews.objects.dates('updated', 'year')]


def news_list(request):
    # TODO: paginate this
    items = models.SiteNews.objects.all()[0:10]

    ret = jingo.render(
        request, 'sitenews/news_list.html',
        {'title': 'News List',
         'items': items,
         'archives': get_years()})
    return ret


def news(request, news_id, slug):
    item = get_object_or_404(models.SiteNews, pk=news_id)

    ret = jingo.render(
        request, 'sitenews/news.html',
        {'item': item,
         'archives': get_years()})
    return ret


def news_archive_year(request, year):
    year = int(year)
    items = models.SiteNews.objects.filter(updated__year=year)

    ret = jingo.render(
        request, 'sitenews/news_list.html',
        {'title': 'News List - %s' % year,
         'items': items,
         'archives': get_years(),
         'activeyear': year})
    return ret
