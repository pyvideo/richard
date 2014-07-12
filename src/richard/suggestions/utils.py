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
from richard.suggestions.models import Suggestion


def mark_if_spam(suggestion):
    """
    Accepts a suggestion instance and checks it's name and comment
    fields for spam words specified in `settings.SPAM_WORDS`.

    If any words are found, it marks the item's state as spam.
    """
    if not settings.SPAM_WORDS:
        return suggestion

    s = ' '.join([suggestion.name, suggestion.comment])
    unique_words = set(
        ''.join(c for c in s.lower() if c.isalnum() or c.isspace()).split())

    for word in settings.SPAM_WORDS:
        if word in unique_words:
            suggestion.state = Suggestion.STATE_SPAM
            suggestion.save()
            break
    return suggestion
