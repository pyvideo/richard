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

import unittest

from nose.tools import eq_

from richard.base.templatetags.batch import batch
from richard.base.templatetags.duration import duration


class BatchFilterTest(unittest.TestCase):
    def test_batch(self):
        eq_(batch([], '2'), [])
        eq_(batch([1, 2, 3, 4, 5], '2'), [[1, 2], [3, 4], [5]])
        eq_(batch([1, 2, 3, 4, 5], '3'), [[1, 2, 3], [4, 5]])

    def test_batch_edgecases(self):
        eq_(batch([1, 2, 3, 4, 5], '0'), [])
        eq_(batch([1, 2, 3, 4, 5], '1'), [1, 2, 3, 4, 5])

    def test_padwith(self):
        eq_(batch([1, 2, 3, 4, 5], '2,FOO'), [[1, 2], [3, 4], [5, 'FOO']])


class DurationFilterTest(unittest.TestCase):
    def test_seconds(self):
        eq_("00:15", duration('15'))
        eq_("00:01", duration('1'))

    def test_minutes(self):
        eq_("01:01", duration('61'))
        eq_("01:00", duration('60'))
        eq_("02:00", duration('120'))

    def test_hours(self):
        eq_("01:00:00", duration('3600'))
        eq_("01:00:02", duration('3602'))
        eq_("02:00:00", duration('7200'))
        eq_("02:02:00", duration('7320'))
        eq_("02:02:01", duration('7321'))
        eq_("02:02:02", duration('7322'))

    def test_bad(self):
        eq_('', duration(None))
