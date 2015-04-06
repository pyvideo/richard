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
import datetime

from django.utils.six import text_type
from django.utils.text import slugify

import factory
from factory import fuzzy
import pytz

from richard.videos import models


class CategoryFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: text_type(slugify(o.title)))

    class Meta:
        model = models.Category


class SpeakerFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: text_type(slugify(o.name)))

    class Meta:
        model = models.Speaker


class TagFactory(factory.DjangoModelFactory):
    tag = fuzzy.FuzzyText()

    class Meta:
        model = models.Tag


class LanguageFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText()

    class Meta:
        model = models.Language
        django_get_or_create = ('name',)


class VideoFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText()
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = models.Video


class RelatedUrlFactory(factory.DjangoModelFactory):
    video = factory.SubFactory(VideoFactory)
    url = fuzzy.FuzzyText(prefix='http://', length=20, suffix='.com')

    class Meta:
        model = models.RelatedUrl


class VideoUrlStatusFactory(factory.DjangoModelFactory):
    START_DATE = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=14)

    check_date = fuzzy.FuzzyDateTime(start_dt=START_DATE)
    video = factory.SubFactory(VideoFactory)

    class Meta:
        model = models.VideoUrlStatus
        exclude = ('START_DATE',)
