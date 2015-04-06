# richard -- video index system
# Copyright (C) 2012, 2013, 2014, 2015 richard contributors.  See AUTHORS.
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

from datetime import date, datetime
from textwrap import dedent

from .models import Category, Speaker, Tag, Language, Video


def generate_sampledata(options):
    lang1 = Language.objects.create(name=u'English', iso639_1=u'en')
    lang1.save()

    speak1 = Speaker.objects.create(name=u'Jessica McKellar')
    speak1.save()
    speak2 = Speaker.objects.create(name=u'Asheesh Laroia')
    speak2.save()
    speak3 = Speaker.objects.create(name=u'Jacob Kaplan-Moss')
    speak3.save()

    tag1 = Tag.objects.create(tag=u'documentation')
    tag1.save()
    tag2 = Tag.objects.create(tag=u'sphinx')
    tag2.save()

    pycon2011 = Category.objects.create(
        title=u'PyCon US 2011',
        slug=u'pycon-us-2011',
        description=u'PyCon US 2011 in Atlanta, GA',
        url=u'http://us.pycon.org/2011/home/')
    pycon2011.save()

    pycon2012 = Category.objects.create(
        title=u'PyCon US 2012',
        slug=u'pycon-us-2012',
        description=u'PyCon US 2012 in Santa Clara, CA',
        url=u'http://us.pycon.org/2012/')
    pycon2012.save()

    vid1 = Video.objects.create(
        state=Video.STATE_LIVE,
        category=pycon2011,
        title=u'Writing great documentation',
        summary=dedent(u"""\
        Writing great documentation

        Presented by Jacob Kaplan-Moss
        """),
        description=dedent(u"""\
        This talk looks at tips, tools and techniques that you can use
        to produce great technical documentation.
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
        )
    )
    vid1.save()
    vid1.speakers.add(speak3)
    vid1.tags.add(tag1, tag2)

    vid2 = Video.objects.create(
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
        thumbnail_url=u'http://img.youtube.com/vi/QrITN6GZDu4/hqdefault.jpg')
    vid2.save()
    vid2.speakers.add(speak1, speak2)

    vid3 = Video.objects.create(
        state=Video.STATE_DRAFT,
        category=pycon2012,
        title=u'Draft video',
        summary=u'This is a draft',
        recorded=date(2012, 3, 11),
        updated=datetime(2012, 3, 13, 16, 15, 17))
    vid3.save()
