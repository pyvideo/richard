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

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from sitenews.models import SiteNews


class NewsFeed(Feed):

    def link(self):
        return reverse('sitenews-feed')

    def items(self):
        return SiteNews.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary + item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.created
