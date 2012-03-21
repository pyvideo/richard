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

from django.contrib import admin
from sitenews.models import SiteNews, Notification


class SiteNewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('title', 'author', 'created')
    list_filter = ('author', )
    search_fields = ('title', 'summary', 'content')


admin.site.register(SiteNews, SiteNewsAdmin)


class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_date'
    list_display = ('interjection', 'start_date', 'end_date')


admin.site.register(Notification, NotificationAdmin)
