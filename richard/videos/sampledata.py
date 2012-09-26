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

from datetime import datetime, date

from richard.videos.models import Video
from richard.videos.tests import category_kind, category, speaker, tag, video


def generate_sampledata(options):
    conference = category_kind(name=u'Conference', save=True)

    pycon2011 = category(name=u'PyCon', title=u'Pycon 2011', slug=u'pycon-2011',
                         description=u'PyCon 2011 in Atlanta, GA',
                         kind=conference, url=u'http://us.pycon.org/2011/home/',
                         save=True)

    pycon2012 = category(name=u'PyCon', title=u'Pycon 2012', slug=u'pycon-2012',
                         description=u'PyCon 2011 in Santa Clara, CA',
                         kind=conference, url=u'http://us.pycon.org/2012/',
                         save=True)

    jm = speaker(name=u'Jessica McKellar', save=True)
    al = speaker(name=u'Asheesh Laroia', save=True)
    jkm = speaker(name=u'Jacob Kaplan-Moss', save=True)

    tag1 = tag(tag=u'documentation', save=True)
    tag2 = tag(tag=u'sphinx', save=True)

    v = video(
        state=Video.STATE_LIVE, category=pycon2011,
        title=u'Writing great documentation',
        summary=u'<p>Writing great documentation</p>'
                u'<p>Presented by Jacob Kaplan-Moss</p>',
        description=u'<p>This talk looks at tips, tools, and techniques you can'
                    u'use to produce great technical documentation.</p>',
        copyright_text=u'Creative Commons Attribution-NonCommercial-ShareAlike 3.0',

        recorded=date(2011, 3, 11),
        updated=datetime(2011, 3, 14, 3, 47, 59),
        source_url=u'http://blip.tv/file/4881071',
        video_mp4_url=u'http://blip.tv/file/get/Pycon-PyCon2011WritingGreatDocumentation191.mp4',
        video_ogv_length=158578172, 
        video_ogv_url=u'http://blip.tv/file/get/Pycon-PyCon2011WritingGreatDocumentation312.ogv',
        thumbnail_url=u'http://a.images.blip.tv/Pycon-PyCon2011WritingGreatDocumentation902.png',
        save=True)

    v.speakers.add(jkm)
    v.tags.add(tag1, tag2)

    v = video(
        state=Video.STATE_LIVE, category=pycon2012,
        title=u'Diversity in practice: How the Boston Python User Group grew to '
              u'1700 people and over 15% women',
        summary=u"""
            <p>How do you bring more women into programming communities with
            long-term, measurable results? In this talk we'll analyze our
            successful effort, the Boston Python Workshop, which brought over
            200 women into Boston's Python community this year.</p>""",

        recorded=date(2012, 3, 11),
        updated=datetime(2012, 3, 13, 16, 15, 17),
        source_url=u'https://www.youtube.com/watch?v=QrITN6GZDu4',
        embed=u'''
            <object width="425" height="344">
            <param name="movie" value="http://www.youtube.com/v/QrITN6GZDu4&amp;hl=en&amp;fs=1">
            <param name="allowFullScreen" value="true">
            <param name="allowscriptaccess" value="always">
            <embed src="http://www.youtube.com/v/QrITN6GZDu4&amp;hl=en&amp;fs=1" allowscriptaccess="always" height="344" width="425" allowfullscreen="true" type="application/x-shockwave-flash"></embed>
            </object>''',
        thumbnail_url=u'http://img.youtube.com/vi/QrITN6GZDu4/hqdefault.jpg',
        save=True)

    v.speakers.add(jm, al)
