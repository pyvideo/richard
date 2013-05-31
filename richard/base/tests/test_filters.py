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

from richard.base.context_processors import duration


class DurationFilterTest(unittest.TestCase):
    def test_seconds(self):
        self.assertEquals("00:15", duration('15'))
        self.assertEquals("00:01", duration('1'))

    def test_minutes(self):
        self.assertEquals("01:01", duration('61'))
        self.assertEquals("01:00", duration('60'))
        self.assertEquals("02:00", duration('120'))

    def test_hours(self):
        self.assertEquals("01:00:00", duration('3600'))
        self.assertEquals("01:00:02", duration('3602'))
        self.assertEquals("02:00:00", duration('7200'))
        self.assertEquals("02:02:00", duration('7320'))
        self.assertEquals("02:02:01", duration('7321'))
        self.assertEquals("02:02:02", duration('7322'))

    def test_bad(self):
        self.assertEquals('', duration(None))
