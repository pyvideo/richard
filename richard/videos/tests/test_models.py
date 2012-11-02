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

from django.test import TestCase
from nose.tools import eq_

from richard.videos.tests import video


class TestVideoModel(TestCase):
    def test_slug_creation(self):
        v = video(title=u'Foo Bar Baz', save=True)
        eq_(v.slug, 'foo-bar-baz')

        v = video(title=u'Foo Bar Baz', slug='baz', save=True)
        eq_(v.slug, 'baz')
