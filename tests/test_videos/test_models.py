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
from httmock import urlmatch, HTTMock
from nose.tools import eq_

from . import factories
from richard.videos import models


class TestVideoModel(TestCase):
    def test_slug_creation(self):
        v = factories.VideoFactory(title=u'Foo Bar Baz')
        eq_(v.slug, 'foo-bar-baz')

        v = factories.VideoFactory(title=u'Foo Bar Baz', slug='baz')
        eq_(v.slug, 'baz')


class TestVideoUrlStatusModel(TestCase):
    @staticmethod
    @urlmatch(netloc='500.com')
    def bad_500(url, request):
        return {'status_code': 500,
                'reason': 'Server error'}

    @staticmethod
    @urlmatch(netloc='400.com')
    def bad_404(url, request):
        return {'status_code': 404,
                'reason': 'Not Found'}

    @staticmethod
    @urlmatch(netloc='200.com')
    def ok_200(url, request):
        return {'status_code': 200,
                'content': 'some shiney content'}

    def test_good_video(self):
        with HTTMock(self.ok_200), HTTMock(self.bad_404), HTTMock(self.bad_500):
            vid = factories.VideoFactory(title=u'Foo', source_url='http://200.com')
            result = models.VideoUrlStatus.objects.create_for_video(vid)
        eq_(result, {})

    def test_bad_video(self):
        with HTTMock(self.ok_200), HTTMock(self.bad_404), HTTMock(self.bad_500):
            vid = factories.VideoFactory(title=u'Foo', source_url='http://400.com')
            result = models.VideoUrlStatus.objects.create_for_video(vid)
        eq_(result, {404: 1})

    def test_bad_video_multiple_links(self):
        with HTTMock(self.ok_200), HTTMock(self.bad_404), HTTMock(self.bad_500):
            vid = factories.VideoFactory(title=u'Foo',
                                         source_url='http://400.com',
                                         thumbnail_url='http://500.com',
                                         video_ogv_url='http://200.com',
                                         video_mp4_url='http://400.com',
                                         video_flv_url='http://400.com')
            result = models.VideoUrlStatus.objects.create_for_video(vid)
        eq_(result, {404: 3,
                     500: 1})
