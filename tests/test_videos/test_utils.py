# -*- coding: utf-8 -*-
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
from nose.tools import eq_

from . import video
from richard.videos.utils import generate_unique_slug


class TestGenerateUniqueSlug(TestCase):
    def test_slug_creation(self):
        """Slug is based on title."""
        v = video(title=u'Foo Bar')
        eq_(generate_unique_slug(v, u'title', u'slug'),
            u'foo-bar')

    def test_unique_slug(self):
        """Generate unique slug using incrementing ending."""
        # These all have the same title, so they get increasingly
        # lame slugs.
        video(title=u'Foo', save=True)
        video(title=u'Foo', save=True)
        video(title=u'Foo', save=True)
        video(title=u'Foo', save=True)
        video(title=u'Foo', save=True)

        v2 = video(title=u'Foo')
        eq_(generate_unique_slug(v2, u'title', u'slug'),
            u'foo-4')

    def test_unicode_title(self):
        v = video(title=u'Nebenläufige Programme mit Python')
        eq_(generate_unique_slug(v, u'title', u'slug'),
            u'nebenlaufige-programme-mit-python')
