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
from videos.models import Video, Category, Speaker, CategoryKind


class CategoryKindAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(CategoryKind, CategoryKindAdmin)


class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'recorded'
    list_display = ('title', 'category', 'state')
    list_filter = ('state', 'category')
    search_fields = ('title', )


admin.site.register(Video, VideoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'linked_url')
    search_fields = ('name', 'title', 'description')

    def linked_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)
    linked_url.allow_tags = True
    linked_url.short_description = 'URL'


admin.site.register(Category, CategoryAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(Speaker, SpeakerAdmin)
