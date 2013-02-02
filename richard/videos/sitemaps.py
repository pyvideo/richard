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

from django.contrib.sitemaps import GenericSitemap

from richard.videos.models import Category, Speaker, Video


CategorySitemap = GenericSitemap({'queryset': Category.objects.all()})
SpeakerSitemap = GenericSitemap({'queryset': Speaker.objects.all()})
VideoSitemap = GenericSitemap({'queryset': Video.objects.live(),
                               'date_field': 'updated'},
                              priority=0.8)

# TODO add sitemap for tags once they have their own page
