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

from django.shortcuts import render

from suggestions.models import Suggestion


def overview(request):
    """Show a list of all accepted suggestions and their status."""
    open_states = (Suggestion.STATE_NEW, Suggestion.STATE_IN_PROGRESS)
    resolved_states = (Suggestion.STATE_COMPLETED, Suggestion.STATE_REJECTED)

    open_objs = Suggestion.objects.filter(state__in=open_states)
    resolved_objs = Suggestion.objects.filter(state__in=resolved_states)

    ret = render(
        request, 'suggestions/list.html',
        {'open_suggestions': open_objs,
         'resolved_suggestions': resolved_objs})
    return ret
