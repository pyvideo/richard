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
