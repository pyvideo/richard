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

from django.core.urlresolvers import reverse

from . import category, speaker, video
from richard.tests.utils import ViewTestCase


class VideosViewsTest(ViewTestCase):
    """Tests for the ``videos`` app."""

    # category 

    def test_category_list_empty(self):
        """Test the view of the listing of all categories."""
        url = reverse('videos-category-list')

        self.assert_HTTP_200(url)
        self.assert_used_templates(
            url, templates=['videos/category_list.html'])

    def test_category_list_with_categories(self):
        """Test the view of the listing of all categories."""
        category(save=True)
        category(save=True)
        category(save=True)

        url = reverse('videos-category-list')

        self.assert_HTTP_200(url)
        self.assert_used_templates(
            url, templates=['videos/category_list.html'])
        
    def test_category_urls(self):
        """Test the view of an category."""
        cat = category(save=True)
        url = cat.get_absolute_url()

        self.assert_HTTP_200(url)
        self.assert_used_templates(
            url, templates=['videos/category.html'])

        # with slug and /
        url = u'/category/%s/%s/' % (cat.id, cat.slug)
        self.assert_HTTP_200(url)

        # with slug and no /
        url = u'/category/%s/%s' % (cat.id, cat.slug)
        self.assert_HTTP_200(url)

        # no slug and /
        url = u'/category/%s/' % cat.id
        self.assert_HTTP_200(url)

        # no slug and no /
        url = u'/category/%s' % cat.id
        self.assert_HTTP_200(url)

    def test_category_raise_404_when_does_not_exist(self):
        """
        Test that trying to view a non-existent category returns 
        a HTTP 404 error.
        """
        url = reverse('videos-category',
                      args=(1234, 'slug'))

        self.assert_HTTP_404(url)

    # speaker

    def test_speaker_list_with_no_speakers_in_database(self):
        """Test the view of the listing of all speakers."""
        url = reverse('videos-speaker-list')

        self.assert_HTTP_200(url)
        self.assert_used_templates(url, 
                                   templates=['videos/speaker_list.html'])

    def test_speaker_list_empty_character(self):
        """
        Test the view of the listing of all speakers given a empty
        `character` GET parameter. It should fallback to showing the 
        speakers starting from the lowest possible character.
        """
        speaker(name='Random Speaker', 
                save=True,)
        spe = speaker(name='Another Speaker', 
                      save=True,)

        url = reverse('videos-speaker-list')
        data = {'character': ''}
        
        self.assert_HTTP_200(url, data) 
        self.assert_used_templates(url, 
                                   data,
                                   templates=['videos/speaker_list.html'])
        self.assert_contains(url, data, text=spe.name)

    def test_speaker_list_character(self):
        """
        Test the view of the listing of all speakers whose names start
        with certain character.
        """
        speaker(name='Another Speaker', 
                save=True,)
        spe = speaker(name='Random Speaker', 
                      save=True,)

        url = reverse('videos-speaker-list')
        data = {'character': 'r'} 

        self.assert_HTTP_200(url, data)
        self.assert_used_templates(url, 
                                   data, 
                                   templates=['videos/speaker_list.html'])
        self.assert_contains(url, data, text=spe.name)

    def test_speaker_list_character_with_string(self):
        """
        Test the view of the listing of all speakers giving a invalid
        character argument. The view should fallback to showing the 
        speakers starting from the lowest possible character.
        """
        speaker(name='Random Speaker', 
                save=True,)
        spe = speaker(name='Another Speaker', 
                      save=True,)

        url = reverse('videos-speaker-list')
        data = {'character': 'richard'}

        self.assert_HTTP_200(url, data)
        self.assert_used_templates(url, 
                                   data, 
                                   templates=['videos/speaker_list.html'])
        self.assert_contains(url, data, text=spe.name)

    def test_speaker_list_not_string_character(self):
        """
        Test the view of the listing of all speakers giving a invalid
        character argument. The view should fallback to showing the 
        speakers starting from the lowest possible character.
        """
        speaker(name='Random Speaker', 
                save=True,)
        spe = speaker(name='Another Speaker', 
                      save=True,)

        url = reverse('videos-speaker-list')
        data = {'character': 42}

        self.assert_HTTP_200(url, data)
        self.assert_used_templates(url, 
                                   data, 
                                   templates=['videos/speaker_list.html'])
        self.assert_contains(url, data, text=spe.name)

    def test_speaker_urls(self):
        """Test the view of a speaker."""
        spe = speaker(name='Random Speaker', save=True)

        # `url.get_absolute_url` returns the URL with the PK and the slug
        url = spe.get_absolute_url()

        self.assert_HTTP_200(url)
        self.assert_used_templates(
            url, templates=['videos/speaker.html'])

        # with slug and /
        url = u'/speaker/%s/%s/' % (spe.id, spe.slug)
        self.assert_HTTP_200(url)

        # with slug and no /
        url = u'/speaker/%s/%s' % (spe.id, spe.slug)
        self.assert_HTTP_200(url)

        # no slug and /
        url = u'/speaker/%s/' % spe.id
        self.assert_HTTP_200(url)

        # no slug and no /
        url = u'/speaker/%s' % spe.id
        self.assert_HTTP_200(url)

    # videos

    def test_video_urls(self):
        """Test the view of a video."""
        vid = video(save=True)
        url = vid.get_absolute_url()

        self.assert_HTTP_200(url)
        self.assert_used_templates(
            url, templates=['videos/video.html'])

        # with slug and /
        url = u'/video/%s/%s/' % (vid.id, vid.slug)
        self.assert_HTTP_200(url)

        # with slug and no /
        url = u'/video/%s/%s' % (vid.id, vid.slug)
        self.assert_HTTP_200(url)

        # no slug and /
        url = u'/video/%s/' % vid.id
        self.assert_HTTP_200(url)

        # no slug and no /
        url = u'/video/%s' % vid.id
        self.assert_HTTP_200(url)

    # search

    def test_search(self):
        """Test the search view."""
        url = reverse('haystack-search')

        self.assert_HTTP_200(url)
