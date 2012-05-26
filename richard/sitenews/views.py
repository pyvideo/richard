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

from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic.detail import DetailView

from richard.sitenews import models


def get_years():
    return [d.year for d in models.SiteNews.objects.dates('updated', 'year')]


class NewsList(ArchiveIndexView):
    model = models.SiteNews
    template_name = 'sitenews/news_list.html'
    context_object_name = 'items'
    date_field = 'updated'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['archives'] = get_years()
        return context


news_list = NewsList.as_view()


class NewsDetail(DetailView):
    model = models.SiteNews
    template_name = 'sitenews/news.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['archives'] = get_years()
        return context


news = NewsDetail.as_view()


class NewsYear(YearArchiveView):
    model = models.SiteNews
    template_name = 'sitenews/news_list.html'
    context_object_name = 'items'
    date_field = 'updated'
    make_object_list = True

    def get_context_data(self, **kwargs):
        context = super(YearArchiveView, self).get_context_data(**kwargs)
        context['archives'] = get_years()
        context['activeyear'] = int(self.get_year())
        return context


news_archive_year = NewsYear.as_view()
