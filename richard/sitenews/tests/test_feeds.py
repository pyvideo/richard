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

from django.core.urlresolvers import reverse
from django.test import TestCase

from nose.tools import eq_

from richard.sitenews.feeds import NewsFeed
from richard.sitenews.tests import sitenews


class FeedTest(TestCase):
    def test_sitenews_feed(self):
        feed = NewsFeed()
        sitenews(save=True)

        eq_(len(feed.items()), 1)

        resp = self.client.get(reverse('sitenews-feed'))
        eq_(resp.status_code, 200)
