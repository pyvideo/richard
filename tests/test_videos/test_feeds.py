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
from django.template.loader import get_template
from django.template.base import TemplateDoesNotExist
from django.test import TestCase

from nose.tools import eq_

from richard.videos.feeds import CategoryFeed
from richard.videos.models import Video
from . import category, video, speaker


class FeedTest(TestCase):

    def test_category_feed(self):
        """Tests for Category rss feed"""

        # Test that only categories with live videos are included.
        feed = CategoryFeed()

        cat = category(save=True)
        video(category=cat, save=True)
        v2 = video(category=cat, save=True)

        # No live videos, no category in feed
        eq_(len(feed.items()), 0)

        # At least one video is live, category is included
        v2.state = Video.STATE_LIVE
        v2.save()
        eq_([x.pk for x in feed.items()], [cat.pk])

        # Category feed description_template exists.
        found_tpl = True
        try:
            get_template(feed.description_template)
        except TemplateDoesNotExist:
            found_tpl = False
        eq_(found_tpl, True)

        # Category list feeds is accessible.
        resp = self.client.get(reverse('videos-category-feed'))
        eq_(resp.status_code, 200)

        # Category videos feed is accessible.
        resp = self.client.get(
            reverse(
                'videos-category-videos-feed',
                kwargs={'category_id': cat.id, 'slug': cat.slug}))
        eq_(resp.status_code, 200)

        # Category videos feed returns 404, invalid category_id.
        resp = self.client.get(
            reverse(
                'videos-category-videos-feed',
                kwargs={'category_id': 50, 'slug': 'fake-slug'}))
        eq_(resp.status_code, 404)

    def test_speaker_feed(self):
        """Tests for Speaker rss feed"""

        spk = speaker(save=True)

        # Speaker feed is accessible
        resp = self.client.get(
            reverse(
                'videos-speaker-feed',
                kwargs={'speaker_id': spk.id, 'slug': spk.slug}))
        eq_(resp.status_code, 200)

        # Speaker feed returns 404, invalid speaker_id.
        resp = self.client.get(
            reverse(
                'videos-speaker-feed',
                kwargs={'speaker_id': 50, 'slug': 'fake-slug'}))
        eq_(resp.status_code, 404)

    def test_video_feed(self):
        """Tests for Video rss feed"""

        # Video feed is accessible
        resp = self.client.get(reverse('videos-new-feed'))
        eq_(resp.status_code, 200)

    def test_video_feed_enclosures(self):
        """Test for encolures of video feeds"""

        # Since video feeds that has enclosure enabled are inherited from the
        # same base feed class ``BaseVideoFeed``, we only need to create a
        # general enclosure test for it.

        # Note: Feed content tests will be applied against `newly posted video`
        # feeds, for the sake of simplicity.
        feeds_url = reverse('videos-new-feed')

        example_url = 'http://example.com/123456'
        youtube_source_url = 'http://www.youtube.com/watch?v=123456'

        vid = video(state=Video.STATE_LIVE, save=True)

        # No video & source urls specified, no enclosures available in feeds.
        resp = self.client.get(feeds_url)
        self.assertNotContains(resp, 'enclosure')

        # `source_url` specified, but not a youtube url.
        vid.source_url = example_url
        vid.save()
        resp = self.client.get(feeds_url)
        self.assertNotContains(resp, 'enclosure')

        # `source_url` specified, this time a youtube url. Enclosure available.
        vid.source_url = youtube_source_url
        vid.save()
        resp = self.client.get(feeds_url)
        self.assertContains(resp, 'enclosure')
        self.assertContains(resp, youtube_source_url)

        # video urls available, correct urls displayed in feeds.
        vid.video_ogv_url = example_url + '.ogv'
        vid.video_webm_url = example_url + '.webm'
        vid.video_mp4_url = example_url + '.mp4'
        vid.video_flv_url = example_url + '.flv'
        vid.save()
        resp = self.client.get(feeds_url)
        self.assertContains(resp, vid.video_ogv_url)
        self.assertContains(resp, vid.video_webm_url)
        self.assertContains(resp, vid.video_mp4_url)
        self.assertContains(resp, vid.video_flv_url)
