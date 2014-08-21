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

from django.test import TestCase

from . import suggestion
from richard.suggestions.models import Suggestion


class TestSuggestion(TestCase):

    def test_resolved_date_set_upon_save(self):
        """Test that the date is set when the suggestion is closed."""
        s = suggestion(save=True)
        assert s.resolved is None

        s.state = Suggestion.STATE_COMPLETED
        s.save()
        assert s.resolved is not None

    def test_no_resolved_date_for_open_states(self):
        """Test that the date is not set when the state is not closed."""
        s = suggestion(save=True)
        assert s.resolved is None

        s.state = Suggestion.STATE_IN_PROGRESS
        s.save()
        assert s.resolved is None

    def test_wipe_resolved_date_when_reopened(self):
        """Test that date is reset when the suggestion is reopened."""
        s = suggestion(save=True, state=Suggestion.STATE_COMPLETED)
        assert s.resolved is not None

        s.state = Suggestion.STATE_NEW
        s.save()
        assert s.resolved is None
