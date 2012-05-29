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

from richard.suggestions.forms import SuggestionForm
from richard.suggestions.models import Suggestion


def overview(request):
    """Show a list of all accepted suggestions and their status."""
    open_objs = Suggestion.objects.filter(state__in=Suggestion.OPEN_STATES)
    resolved_objs = Suggestion.objects.filter(state__in=Suggestion.RESOLVED_STATES)

    ret = render(
        request, 'suggestions/list.html',
        {'open_suggestions': open_objs,
         'resolved_suggestions': resolved_objs})
    return ret


def submit(request):
    """Submit a new suggestion."""
    success = False
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = SuggestionForm()

    ret = render(
        request, 'suggestions/submit_form.html',
        {'form': form,
         'success': success})
    return ret
