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
from videos.tests import category_kind, category, tag, speaker, video
from videos.models import create_videos


class TestCreatevideo(TestCase):
    def test_create_no_videos(self):
        # Return an empty list if there's nothing to do
        eq_(create_videos([]), [])

    def test_create_one_video(self):
        cat = category(name=u'foo', slug=u'foo')
        cat.save()

        vid = {
            'state': 1,
            'title': u'foo',
            'summary': u'foo',
            'source_url': u'http://example.com/',
            'category': cat.id}
        ret = create_videos([vid])

        eq_(ret[0].title, vid['title'])

    def test_video_with_speakers(self):
        cat = category(name=u'foo', slug=u'foo')
        cat.save()

        speaker_names = [u'Carl Karsten', u'Ryan Verner']
        vid = {
            'state': 1,
            'title': u'foo',
            'summary': u'foo',
            'source_url': u'http://example.com/',
            'category': cat.id,
            'speakers': speaker_names}
        ret = create_videos([vid])

        eq_(ret[0].title, vid['title'])
        speakers = ret[0].speakers.all()
        assert speakers[0].name in speaker_names
        assert speakers[1].name in speaker_names
        assert speakers[0].name != speakers[1].name

    def test_with_existing_speaker(self):
        carl = speaker(name=u'Carl Karsten')
        carl.save()
        speaker_names = [carl.name, u'Phil']

        cat = category(name=u'foo', slug=u'foo')
        cat.save()

        vid = {
            'state': 1,
            'title': u'foo',
            'summary': u'foo',
            'source_url': u'http://example.com/',
            'category': cat.id,
            'speakers': speaker_names}
        ret = create_videos([vid])

        eq_(ret[0].title, vid['title'])
        speakers = ret[0].speakers.order_by('name')[:]
        eq_(speakers[0].name, carl.name)
        eq_(speakers[0].id, carl.id)
        eq_(speakers[1].name, speaker_names[1])

    def test_video_with_tags(self):
        cat = category(name=u'foo', slug=u'foo')
        cat.save()

        t1 = tag(tag=u'tag1')
        t1.save()
        tag_names = [t1.tag, u'tag2']
        vid = {
            'state': 1,
            'title': u'foo',
            'summary': u'foo',
            'source_url': u'http://example.com/',
            'category': cat.id,
            'tags': tag_names}
        ret = create_videos([vid])

        eq_(ret[0].title, vid['title'])
        tags = ret[0].tags.order_by('tag')
        eq_(tags[0].tag, t1.tag)
        eq_(tags[0].id, t1.id)
        eq_(tags[1].tag, tag_names[1])
