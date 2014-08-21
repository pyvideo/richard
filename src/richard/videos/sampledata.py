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

from datetime import datetime, date
from textwrap import dedent

from richard.videos.models import Video
from tests.test_videos import category, speaker, tag, video  # This is horrible and will be refactored


def generate_sampledata(options):
    pycon2011 = category(
        title=u'Pycon 2011',
        slug=u'pycon-2011',
        description=u'PyCon 2011 in Atlanta, GA',
        url=u'http://us.pycon.org/2011/home/',
        save=True)

    pycon2012 = category(
        title=u'Pycon 2012',
        slug=u'pycon-2012',
        description=u'PyCon 2011 in Santa Clara, CA',
        url=u'http://us.pycon.org/2012/',
        save=True)

    sp1 = speaker(name=u'Jessica McKellar', save=True)
    sp2 = speaker(name=u'Asheesh Laroia', save=True)
    sp3 = speaker(name=u'Jacob Kaplan-Moss', save=True)

    tag1 = tag(tag=u'documentation', save=True)
    tag2 = tag(tag=u'sphinx', save=True)

    v = video(
        state=Video.STATE_LIVE, category=pycon2011,
        title=u'Writing great documentation',
        summary=dedent("""\
        Writing great documentation

        Presented by Jacob Kaplan-Moss
        """),
        description=dedent("""\
        This talk looks at tips, tools, and techniques you can
        use to produce great technical documentation.
        """),
        copyright_text=u'CC-SA-NC 3.0',
        recorded=date(2011, 3, 11),
        updated=datetime(2011, 3, 14, 3, 47, 59),
        source_url=u'http://blip.tv/file/4881071',
        video_mp4_url=(
            u'http://05d2db1380b6504cc981-8cbed8cf7e3a131cd8f1c3e383d10041'
            u'.r93.cf2.rackcdn.com/pycon-us-2011/'
            u'403_writing-great-documentation.mp4'
        ),
        thumbnail_url=(
            u'http://a.images.blip.tv/'
            u'Pycon-PyCon2011WritingGreatDocumentation902.png'
        ),
        save=True)

    v.speakers.add(sp3)
    v.tags.add(tag1, tag2)

    v = video(
        state=Video.STATE_LIVE,
        category=pycon2012,
        title=dedent("""\
        Diversity in practice: How the Boston Python User Group grew
        to 1700 people and over 15% women
        """),
        summary=dedent(u"""\
        How do you bring more women into programming communities with
        long-term, measurable results? In this talk we'll analyze our
        successful effort, the Boston Python Workshop, which brought over
        200 women into Boston's Python community this year.
        """),
        recorded=date(2012, 3, 11),
        updated=datetime(2012, 3, 13, 16, 15, 17),
        source_url=u'https://www.youtube.com/watch?v=QrITN6GZDu4',
        embed=dedent("""\
        <object width="425" height="344">
        <param name="movie"
        value="http://www.youtube.com/v/QrITN6GZDu4&amp;hl=en&amp;fs=1">
        <param name="allowFullScreen" value="true">
        <param name="allowscriptaccess" value="always">
        <embed src="http://www.youtube.com/v/QrITN6GZDu4&amp;hl=en&amp;fs=1"
        allowscriptaccess="always" height="344"
        width="425" allowfullscreen="true"
        type="application/x-shockwave-flash"></embed>
        </object>
        """),
        thumbnail_url=u'http://img.youtube.com/vi/QrITN6GZDu4/hqdefault.jpg',
        save=True)

    v.speakers.add(sp1, sp2)

    v = video(
        state=Video.STATE_DRAFT,
        category=pycon2012,
        title=u'Draft video',
        summary=u'This is a draft',
        recorded=date(2012, 3, 11),
        updated=datetime(2012, 3, 13, 16, 15, 17),
        save=True)
