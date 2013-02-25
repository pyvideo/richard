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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from richard.suggestions.forms import SuggestionForm
from richard.suggestions.models import Suggestion
from richard.suggestions.utils import mark_if_spam


@csrf_protect
def suggestions(request):
    """Show a list of all accepted suggestions and their status."""
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            mark_if_spam(obj)
            messages.add_message(request, messages.INFO,
                                 'Suggestion submitted.')
            return redirect('suggestions-list')
    else:
        form = SuggestionForm()

    open_objs = Suggestion.objects.filter(
        state__in=Suggestion.OPEN_STATES,
        is_reviewed=True)
    resolved_objs = Suggestion.objects.filter(
        state__in=Suggestion.RESOLVED_STATES,
        is_reviewed=True)

    ret = render(
        request, 'suggestions/suggestions_list.html',
        {'form': form,
         'open_suggestions': open_objs,
         'resolved_suggestions': resolved_objs})
    return ret
