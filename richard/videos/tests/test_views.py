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

import os
import json
import shutil

from django.conf import settings
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.encoding import smart_text

from nose.tools import eq_

from richard.videos.tests import category, speaker, video, related_url
from richard.videos.models import Video


class TestVideos(TestCase):
    """Tests for the ``videos`` app."""

    # category

    def test_category_list_empty(self):
        """Test the view of the listing of all categories."""
        url = reverse('videos-category-list')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/category_list.html')

    def test_category_list_with_categories(self):
        """Test the view of the listing of all categories."""
        category(save=True)
        category(save=True)
        category(save=True)

        url = reverse('videos-category-list')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/category_list.html')

    def test_category_urls(self):
        """Test the view of an category."""
        cat = category(save=True)

        cases = [
            cat.get_absolute_url(),
            u'/category/%s/%s/' % (cat.id, cat.slug),   # with slug and /
            u'/category/%s/%s' % (cat.id, cat.slug),    # with slug and no /
            u'/category/%s/' % cat.id,                  # no slug and /
            u'/category/%s' % cat.id,                   # no slug and no /
        ]

        for url in cases:
            resp = self.client.get(url)
            eq_(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'videos/category.html')

    def test_category_raise_404_when_does_not_exist(self):
        """
        Test that trying to view a non-existent category returns
        a HTTP 404 error.
        """
        url = reverse('videos-category',
                      args=(1234, 'slug'))

        resp = self.client.get(url)
        eq_(resp.status_code, 404)

    # speaker

    def test_speaker_list_with_no_speakers_in_database(self):
        """Test the view of the listing of all speakers."""
        url = reverse('videos-speaker-list')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/speaker_list.html')

    def test_speaker_list_empty_character(self):
        """
        Test the view of the listing of all speakers given a empty
        `character` GET parameter. It should fallback to showing the
        speakers starting from the lowest possible character.
        """
        s1 = speaker(name=u'Random Speaker', save=True)
        s2 = speaker(name=u'Another Speaker', save=True)

        url = reverse('videos-speaker-list')
        data = {'character': ''}

        resp = self.client.get(url, data)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/speaker_list.html')
        self.assertNotContains(resp, s1.name)
        self.assertContains(resp, s2.name)

    def test_speaker_list_character(self):
        """
        Test the view of the listing of all speakers whose names start
        with certain character.
        """
        s1 = speaker(name=u'Another Speaker', save=True)
        s2 = speaker(name=u'Random Speaker', save=True)

        url = reverse('videos-speaker-list')
        data = {'character': 'r'}

        resp = self.client.get(url, data)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/speaker_list.html')
        self.assertNotContains(resp, s1.name)
        self.assertContains(resp, s2.name)

    def test_speaker_list_character_with_string(self):
        """
        Test the view of the listing of all speakers giving a invalid
        character argument. The view should fallback to showing the
        speakers starting from the lowest possible character.
        """
        s1 = speaker(name=u'Random Speaker', save=True)
        s2 = speaker(name=u'Another Speaker', save=True)

        url = reverse('videos-speaker-list')
        data = {'character': 'richard'}

        resp = self.client.get(url, data)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/speaker_list.html')
        self.assertNotContains(resp, s1.name)
        self.assertContains(resp, s2.name)

    def test_speaker_list_not_string_character(self):
        """
        Test the view of the listing of all speakers giving a invalid
        character argument. The view should fallback to showing the
        speakers starting from the lowest possible character.
        """
        s1 = speaker(name=u'Random Speaker', save=True)
        s2 = speaker(name=u'Another Speaker', save=True)

        url = reverse('videos-speaker-list')
        data = {'character': 42}

        resp = self.client.get(url, data)
        eq_(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'videos/speaker_list.html')
        self.assertNotContains(resp, s1.name)
        self.assertContains(resp, s2.name)

    def test_speaker_urls(self):
        """Test the view of a speaker."""
        spe = speaker(name=u'Random Speaker', save=True)

        cases = [
            spe.get_absolute_url(),     # returns the URL with pk and slug
            u'/speaker/%s/%s/' % (spe.id, spe.slug),    # with slug and /
            u'/speaker/%s/%s' % (spe.id, spe.slug),     # with slug and no /
            u'/speaker/%s/' % spe.id,                   # no slug and /
            u'/speaker/%s' % spe.id,                    # no slug and no /
        ]

        for url in cases:
            resp = self.client.get(url)
            eq_(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'videos/speaker.html')

    # videos

    def test_video_urls(self):
        """Test the view of a video."""
        vid = video(save=True)

        cases = [
            vid.get_absolute_url(),
            u'/video/%s/%s/' % (vid.id, vid.slug),  # with slug and /
            u'/video/%s/%s' % (vid.id, vid.slug),   # with slug and no /
            u'/video/%s/' % vid.id,                 # no slug and /
            u'/video/%s' % vid.id,                  # no slug and no /
        ]

        for url in cases:
            resp = self.client.get(url)
            eq_(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'videos/video.html')

    def test_active_video_speaker_page(self):
        """Active video should show up on it's speaker's page."""
        s = speaker(save=True)
        vid = video(state=Video.STATE_LIVE, save=True)
        vid.speakers.add(s)

        speaker_url = s.get_absolute_url()

        resp = self.client.get(speaker_url)
        self.assertContains(resp, vid.title)

    def test_active_video_category_page(self):
        """Active video should shows up on category page."""
        vid = video(state=Video.STATE_LIVE, save=True)

        category_url = vid.category.get_absolute_url()

        resp = self.client.get(category_url)
        self.assertContains(resp, vid.title)

    def test_inactive_video_category_page(self):
        """Inactive video should not show up on category page."""
        vid = video(save=True)

        category_url = vid.category.get_absolute_url()

        resp = self.client.get(category_url)
        self.assertNotContains(resp, vid.title)

    def test_inactive_video_speaker_page(self):
        """Inactive video should not show up on it's speaker's page."""
        s = speaker(save=True)
        vid = video(save=True)
        vid.speakers.add(s)

        speaker_url = s.get_absolute_url()

        resp = self.client.get(speaker_url)
        self.assertNotContains(resp, vid.title)

    def test_related_url(self):
        """Related urls should show up on the page."""
        v = video(save=True)
        rurl = related_url(video_id=v.id, url=u'http://example.com/foo',
                           description=u'Example related url',
                           save=True)

        resp = self.client.get(v.get_absolute_url())
        self.assertContains(resp, rurl.description)

    def test_download_only(self):
        """Video urls marked as download-only shouldn't be in video tag."""
        v = video(video_ogv_url='http://example.com/OGV_VIDEO',
                  video_ogv_download_only=False,
                  video_mp4_url='http://example.com/MP4_VIDEO',
                  video_mp4_download_only=True,
                  save=True)

        resp = self.client.get(v.get_absolute_url())
        # This shows up in video tag and in downloads area
        eq_(resp.content.count(b'OGV_VIDEO'), 2)
        # This only shows up in downloads area
        eq_(resp.content.count(b'MP4_VIDEO'), 1)


class TestVideoSearch(TestCase):
    def tearDown(self):
        """Remove the search index after each test run.

        The path is set in richard/settings_test.py."""
        path = settings.HAYSTACK_CONNECTIONS['default']['PATH']
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_search(self):
        """Test the search view."""
        url = reverse('videos-search')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)

    def test_opensearch_description(self):
        """Test the opensearch description view."""
        url = reverse('videos-opensearch')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)

    @override_settings(OPENSEARCH_ENABLE_SUGGESTIONS=True)
    def test_opensearch_description_with_suggestions(self):
        """Test the opensearch description view."""
        url = reverse('videos-opensearch')

        resp = self.client.get(url)
        eq_(resp.status_code, 200)

    @override_settings(OPENSEARCH_ENABLE_SUGGESTIONS=True)
    def test_opensearch_suggestions(self):
        """Test the opensearch suggestions view."""
        video(title='introduction to pypy', save=True)
        video(title='django testing', save=True)
        video(title='pycon 2012 keynote', save=True)
        video(title='Speedily Practical Large-Scale Tests', save=True)
        management.call_command('rebuild_index', interactive=False)

        url = reverse('videos-opensearch-suggestions')

        response = self.client.get(url, {'q': 'test'})
        eq_(response.status_code, 200)
        data = json.loads(smart_text(response.content))
        eq_(data[0], 'test')
        eq_(set(data[1]),
            set(['django testing', 'Speedily Practical Large-Scale Tests']))

    def test_opensearch_suggestions_disabled(self):
        """Test that when suggestions are disabled, the view does nothing."""
        url = reverse('videos-opensearch-suggestions')

        response = self.client.get(url, {'q': 'test'})
        eq_(response.status_code, 404)
