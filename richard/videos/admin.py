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

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from richard.videos.models import (Video, Category, Speaker, Tag,
                                   Language, RelatedUrl)


class WhiteboardFilter(SimpleListFilter):
    """Filter objects with whiteboard bits"""
    title = _('whiteboard')
    parameter_name = 'whiteboard'

    def lookups(self, request, model_admin):
        return (
            ('0', _('No')),
            ('1', _('Yes')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(whiteboard__exact='')
        if self.value() == '1':
            return queryset.exclude(whiteboard__exact='')


def make_live(modeladmin, request, queryset):
    queryset.update(state=1)
make_live.short_description = 'Make live'


def make_draft(modeladmin, request, queryset):
    queryset.update(state=2)
make_draft.short_description = 'Make draft'


class RelatedUrlInline(admin.TabularInline):
    model = RelatedUrl


class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'recorded'
    list_display = ('title', 'category', 'whiteboard', 'state')
    list_filter = (WhiteboardFilter, 'state', 'category')
    search_fields = ('title',)
    radio_fields = {'state': admin.HORIZONTAL}
    filter_horizontal = ('tags', 'speakers',)
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RelatedUrlInline]
    actions = [make_live, make_draft]


admin.site.register(Video, VideoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'linked_url', 'whiteboard')
    list_filter = (WhiteboardFilter,)
    search_fields = ('name', 'title', 'description')

    def linked_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)
    linked_url.allow_tags = True
    linked_url.short_description = 'URL'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Speaker, SpeakerAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)


admin.site.register(Tag, TagAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('iso639_1', 'name')
    search_fields = ('name',)


admin.site.register(Language, LanguageAdmin)
