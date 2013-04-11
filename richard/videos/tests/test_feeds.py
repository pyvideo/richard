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

# TODO: Write more

from django.test import TestCase
from nose.tools import eq_

from richard.videos.feeds import CategoryFeed
from richard.videos.models import Video
from richard.videos.tests import category, video


class FeedTest(TestCase):

    def test_category_feed(self):
        """Test that only categories with live videos are included."""
        feed = CategoryFeed()

        cat = category(save=True)
        v1 = video(category=cat, save=True)
        v2 = video(category=cat, save=True)

        # No live videos, no category in feed
        eq_(len(feed.items()), 0)

        # At least one video is live, category is included
        v2.state = Video.STATE_LIVE
        v2.save()
        eq_([x.pk for x in feed.items()], [cat.pk])
