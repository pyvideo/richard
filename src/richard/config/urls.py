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
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

# enable the admin
from django.contrib import admin
admin.autodiscover()
admin.site.login = login_required(admin.site.login)

from richard.pages.sitemaps import PageSitemap
from richard.videos.sitemaps import (
    CategorySitemap, SpeakerSitemap, VideoSitemap)


sitemaps = {
    'page': PageSitemap,
    'category': CategorySitemap,
    'speaker': SpeakerSitemap,
    'video': VideoSitemap
}

urlpatterns = patterns(
    '',

    url(r'', include('richard.base.urls')),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps}),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^pages/', include('richard.pages.urls')),
    url(r'^suggestions/', include('richard.suggestions.urls')),
    url(r'', include('richard.videos.urls')),

    url(r'', include('django_browserid.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
