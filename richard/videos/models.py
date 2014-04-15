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

import collections
import datetime
import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import requests
import requests.exceptions

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from richard.videos.utils import generate_unique_slug


MIMETYPES_MAP = {
    'ogv': 'video/ogg',
    'mp4': 'video/mp4',
    'webm': 'video/webm',
    'flv': 'video/x-flv'
}
USE_MARKDOWN_HELP_TEXT = _(u'Use Markdown')


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(
        max_length=255,
        help_text=_(u'The complete title for the category. e.g. '
                    u'PyCon 2010'))
    description = models.TextField(
        blank=True, default=u'',
        help_text=USE_MARKDOWN_HELP_TEXT)
    url = models.URLField(
        blank=True, default=u'',
        help_text=_(u'URL for the category. e.g. If this category was a '
                    u'conference, this would be the url for the conference '
                    u'web-site.'))
    start_date = models.DateField(
        blank=True, null=True,
        help_text=_(u'If the category was an event, then this is the start '
                    u'date for the event.'))

    whiteboard = models.CharField(
        blank=True, max_length=255, default=u'',
        help_text=_(u'Editor notes for this category.'))

    slug = models.SlugField(unique=True)

    # when the category was added to this site
    added = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Category %s>' % self.title.encode('ascii', 'ignore')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, u'title', u'slug')
        super(Category, self).save(*args, **kwargs)

    class Meta(object):
        ordering = ["title"]
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')

    @models.permalink
    def get_absolute_url(self):
        return ('videos-category', (self.pk, self.slug))


@python_2_unicode_compatible
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Speaker %s: %s>' % (
            self.id, self.name.encode('ascii', 'ignore'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, u'name', u'slug')
        super(Speaker, self).save(*args, **kwargs)

    class Meta(object):
        ordering = ['name']
        verbose_name = _(u'speaker')
        verbose_name_plural = _(u'speakers')

    @models.permalink
    def get_absolute_url(self):
        return ('videos-speaker', (self.pk, self.slug))


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag

    def __repr__(self):
        return '<Tag %s>' % self.tag.encode('ascii', 'ignore')

    class Meta(object):
        ordering = ['tag']
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags')


@python_2_unicode_compatible
class Language(models.Model):
    iso639_1 = models.CharField(max_length=3)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class VideoManager(models.Manager):
    def live(self):
        return self.get_query_set().filter(state=Video.STATE_LIVE)

    def live_order_by_title(self):
        return self.live().order_by('title')


@python_2_unicode_compatible
class Video(models.Model):
    STATE_LIVE = 1
    STATE_DRAFT = 2

    STATE_CHOICES = (
        (STATE_LIVE, u'Live'),
        (STATE_DRAFT, u'Draft'),
        )

    LOCAL_THUMBNAIL_PATH = 'video/thumbnails/%d.jpg'

    state = models.IntegerField(choices=STATE_CHOICES, default=STATE_DRAFT)

    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, default=u'',
                               help_text=USE_MARKDOWN_HELP_TEXT)
    description = models.TextField(blank=True, default=u'',
                                   help_text=USE_MARKDOWN_HELP_TEXT)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category)
    speakers = models.ManyToManyField(Speaker, blank=True)

    # notes for quality issues (audio or video) in the video
    quality_notes = models.TextField(blank=True, default=u'')

    # the primary language the video is in
    language = models.ForeignKey(Language, null=True)

    # text for copyright/license--for now it's loose form.
    # if null, use source video link.
    # TODO: rename this to license
    copyright_text = models.TextField(blank=True)

    # embed for flash player things
    embed = models.TextField(blank=True)

    # url for the thumbnail
    thumbnail_url = models.URLField(max_length=255, null=True, blank=True)

    # duration in seconds
    duration = models.IntegerField(null=True, blank=True, help_text='In seconds')

    # TODO: fix this- each video type should have a filesize

    # TODO: add video_m4v

    # these are downloadable urls
    video_ogv_length = models.IntegerField(null=True, blank=True)
    video_ogv_url = models.URLField(max_length=255, null=True, blank=True)
    video_ogv_download_only = models.BooleanField(default=False)
    video_mp4_length = models.IntegerField(null=True, blank=True)
    video_mp4_url = models.URLField(max_length=255, null=True, blank=True)
    video_mp4_download_only = models.BooleanField(default=False)
    video_webm_length = models.IntegerField(null=True, blank=True)
    video_webm_url = models.URLField(max_length=255, null=True, blank=True)
    video_webm_download_only = models.BooleanField(default=False)
    video_flv_length = models.IntegerField(null=True, blank=True)
    video_flv_url = models.URLField(max_length=255, null=True, blank=True)
    video_flv_download_only = models.BooleanField(default=False)

    # source url in case we need to find things again
    source_url = models.URLField(max_length=255, null=True, blank=True)

    # whiteboard for editor notes
    whiteboard = models.CharField(max_length=255, blank=True, default=u'')

    # when the video was originally recorded
    recorded = models.DateField(null=True, blank=True)

    # when the video was added to this site
    added = models.DateTimeField(auto_now_add=True)

    # when the video metadata was last updated
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True)

    objects = VideoManager()

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Video %s (%s)>' % (self.title[:30].encode('ascii', 'ignore'),
                                    self.category)

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = generate_unique_slug(self, u'title', u'slug')
        super(Video, self).save(*args, **kwargs)

    class Meta(object):
        get_latest_by = 'recorded'
        ordering = ['-recorded', 'title']
        verbose_name = _(u'video')
        verbose_name_plural = _(u'videos')

    @models.permalink
    def get_absolute_url(self):
        return ('videos-video', (self.pk, self.slug))

    def get_thumbnail_url(self):
        """Find a thumbnail for this video in the following order:

        1. use a local image
        2. use the remote image in `thumbnail_url`
        3. show a placeholder image
        """
        no_thumbnail = settings.STATIC_URL + 'videos/img/no_thumbnail.png'

        local_path = self.LOCAL_THUMBNAIL_PATH % self.pk
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, local_path)):
            return settings.MEDIA_URL + local_path
        else:
            return self.thumbnail_url or no_thumbnail

    @property
    def thumbnail_width(self):
        return settings.VIDEO_THUMBNAIL_SIZE[0]

    @property
    def thumbnail_height(self):
        return settings.VIDEO_THUMBNAIL_SIZE[1]

    def is_live(self):
        return self.state == self.STATE_LIVE

    def get_all_formats(self):
        """Return formats ordered by MEDIA_PREFERENCE setting.

        Looks through all video_url/video_length fields on the model and
        selects those that are available, i.e. that have a value. The
        elements in the returned list are ordered by their format.

        """
        result = []
        for fmt in settings.MEDIA_PREFERENCE:
            url = getattr(self, 'video_%s_url' % fmt, None)

            # skip empty urls and unsupported formats
            if not url:
                continue

            try:
                mime_type = MIMETYPES_MAP[fmt]
            except KeyError:
                raise LookupError('No mimetype registered for "%s"' % fmt)

            result.append({
                'url': url,
                'length': getattr(self, 'video_%s_length' % fmt),
                'display': mime_type.split('/')[1],
                'mime_type': mime_type,
                'download_only': getattr(self, 'video_%s_download_only' % fmt),
            })

        return result

    def get_html5_formats(self):
        """Gets all formats appropriate for html5 video tag"""
        return [fmt for fmt in self.get_all_formats()
                if not fmt['download_only']]

    def is_youtube(self):
        """Is this a video on YouTube?"""
        if not self.source_url:
            return False
        parsed = urlparse(self.source_url.lower())
        return 'youtube' in parsed.netloc or 'youtu.be' in parsed.netloc

    def get_feed_formats(self):
        """Gets all formats appropriate for feed

        Note: We if this video is on YouTube, we add the YouTube url
        to the available formats because we want to make sure this
        works with Miro. We put it last in the list because most
        options are # better than this one.

        """
        fmts = self.get_all_formats()
        if self.is_youtube():
            fmts.append({
                'url': self.source_url,
                'mime_type': 'video/flv',
            })
        return fmts

    def get_download_formats(self):
        """Gets all formats appropriate for file download list"""
        return self.get_all_formats()

    @property
    def all_urls(self):
        """Returns a list of all the populated URLs of this Video
        """
        return [url for url in
                [
                    self.thumbnail_url,
                    self.video_ogv_url,
                    self.video_mp4_url,
                    self.video_webm_url,
                    self.video_flv_url,
                    self.source_url,
                ]
                if url is not None and url != ''
        ]


@python_2_unicode_compatible
class RelatedUrl(models.Model):
    video = models.ForeignKey(Video, related_name='related_urls')
    url = models.URLField(max_length=255)
    description = models.CharField(max_length=255, blank=True, default=u'')

    def __str__(self):
        return self.url

    def __repr__(self):
        return '<URL %s>' % self.url

    def display(self):
        """For showing the url

        This reduces long urls to 50 characters for display.

        """
        return self.url[:50]


class VideoUrlStatusManager(models.Manager):
    def create_for_video(self, video):
        """Create VideoUrlStatus objects for each failed url in a video

        :return: The number of VidoeUrlStatuses created
        """
        def check_urls(urls):
            for url in urls:
                try:
                    r = requests.head(url)
                    if not r.ok:
                        yield url, r.status_code, r.reason
                except requests.exceptions.RequestException as e:
                    yield url, 9999, unicode(e)

        video_url_status = [
            VideoUrlStatus(
                video=video,
                url=url,
                check_date=datetime.datetime.now(),
                status_code=status_code,
                status_message=status_message)
            for url, status_code, status_message in check_urls(video.all_urls)
        ]
        if video_url_status:
            self.bulk_create(video_url_status)
        return collections.Counter(video.status_code for video in video_url_status)


class VideoUrlStatus(models.Model):
    objects = VideoUrlStatusManager()

    check_date = models.DateTimeField(null=False, blank=False)
    status_code = models.IntegerField(null=False, blank=False)
    status_message = models.CharField(max_length=255, null=False, blank=True)
    url = models.URLField(max_length=255, null=False, blank=False)
    video = models.ForeignKey(Video)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'


class ShrodingersSlugRelatedField(serializers.SlugRelatedField):
    """Less fussy SlugRelatedField

    It's just like SlugRelatedField, but allows for the object not to
    exist. If it doesn't exist, then it'll get created.

    """
    def from_native(self, data):
        data = data.strip()
        if self.queryset is None:
            raise Exception('Need "queryset" argument')
        try:
            return self.queryset.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            obj = self.queryset.model(**{self.slug_field: data})
            obj.save()
            return obj
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=False, slug_field='title')
    language = serializers.SlugRelatedField(
        many=False, required=False, slug_field='name')
    slug = serializers.SlugField(read_only=True)

    # These are a little funky since we denormalize them for the API.
    speakers = ShrodingersSlugRelatedField(many=True, slug_field='name')
    tags = ShrodingersSlugRelatedField(many=True, slug_field='tag')

    class Meta:
        model = Video


