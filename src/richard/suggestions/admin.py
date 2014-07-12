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

from richard.suggestions.models import Suggestion


def mark_as_spam(modeladmin, request, queryset):
    queryset.update(state=Suggestion.STATE_SPAM,
                    is_reviewed=True)


def mark_as_reviewed(modeladmin, request, queryset):
    queryset.update(is_reviewed=True)


class SuggestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'submitted'
    list_display = ('state', 'is_reviewed', 'name', 'url', 'submitted',
                    'resolved')
    list_filter = ('state', 'is_reviewed',)
    search_fields = ('name', 'url',)
    radio_fields = {'state': admin.HORIZONTAL}
    exclude = ('resolved',)
    actions = [mark_as_spam, mark_as_reviewed]


admin.site.register(Suggestion, SuggestionAdmin)
