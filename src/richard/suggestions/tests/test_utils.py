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
from django.test.utils import override_settings

from nose.tools import eq_

from richard.suggestions import utils
from richard.suggestions.models import Suggestion
from richard.suggestions.tests import suggestion


class TestMarkIfSpam(TestCase):
    """Tests for mark_if_spam."""

    def test_mark_if_spam_no_spam_words(self):
        s = suggestion(name='foo', comment='foo', save=True)
        utils.mark_if_spam(s)

        eq_(s.state, Suggestion.STATE_NEW)

    @override_settings(SPAM_WORDS=['foo'])
    def test_mark_if_spam_with_words(self):
        # handle name
        s = suggestion(name='1 foo 2', comment='1 bar 2', save=True)
        utils.mark_if_spam(s)

        eq_(s.state, Suggestion.STATE_SPAM)

        # handle comment
        s = suggestion(name='1 bar 2', comment='1 foo 2', save=True)
        utils.mark_if_spam(s)

        eq_(s.state, Suggestion.STATE_SPAM)

        # not case-sensitive
        s = suggestion(name='1 FOO 2', comment='1 FOO 2', save=True)
        utils.mark_if_spam(s)

        eq_(s.state, Suggestion.STATE_SPAM)

        # don't flag superstrings
        s = suggestion(name='1 food 2', comment='1 food 2', save=True)
        utils.mark_if_spam(s)

        eq_(s.state, Suggestion.STATE_NEW)
