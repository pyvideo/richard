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

import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify


USE_HTML_HELP_TEXT = "Use HTML."


class CategoryKind(models.Model):
    name = models.CharField(max_length=40)


class Category(models.Model):
    kind = models.ForeignKey(CategoryKind)

    name = models.CharField(
        max_length=255,
        help_text='The name of the category. e.g. PyCon')
    title = models.CharField(
        max_length=255,
        help_text='The complete title for the category. e.g. '
        'PyCon 2010')
    description = models.TextField(
        blank=True, default=u'',
        help_text=USE_HTML_HELP_TEXT)
    url = models.URLField(
        blank=True, default=u'',
        help_text='URL for the category. e.g. If this category was a '
        'conference, this would be the url for the conference '
        'web-site.')
    start_date = models.DateField(
        null=True,
        help_text='If the category was an event, then this is the start '
        'date for the event.')

    whiteboard = models.TextField(
        blank=True, default=u'',
        help_text='Editor notes for this category.')

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return '<Category %s>' % self.title

    class Meta(object):
        ordering = ["name", "title"]

    @models.permalink
    def get_absolute_url(self):
        return ('videos-category', (self.pk, self.slug))


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return '<Speaker %s: %s>' % (self.id, self.name)

    class Meta(object):
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('videos-speaker', (self.pk, self.slug))


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __unicode__(self):
        return '<Tag %s>' % self.tag

    class Meta(object):
        ordering = ['tag']


class Video(models.Model):
    STATE_LIVE = 1
    STATE_DRAFT = 2

    STATE_CHOICES = (
        (STATE_LIVE, u'Live'),
        (STATE_DRAFT, u'Draft'),
        )

    LOCAL_THUMBNAIL_PATH = 'video/%d.jpg'

    # TODO: this shouldn't default to null--this should default to
    # draft
    state = models.IntegerField(choices=STATE_CHOICES, null=True)

    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, default=u'',
                               help_text=USE_HTML_HELP_TEXT)
    description = models.TextField(blank=True, default=u'',
                                   help_text=USE_HTML_HELP_TEXT)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    speakers = models.ManyToManyField(Speaker)

    # notes for quality issues (audio or video) in the video
    quality_notes = models.TextField(blank=True, default=u'',
                                     help_text=USE_HTML_HELP_TEXT)

    # text for copyright/license--for now it's loose form.
    # if null, use source video link.
    # TODO: rename this to license
    copyright_text = models.TextField(null=True)

    # embed for flash player things
    embed = models.TextField(null=True, blank=True)

    # url for the thumbnail
    thumbnail_url = models.URLField(max_length=255, null=True)

    # TODO: fix this--there should be one duration in seconds and then
    # each video type should have a filesize

    # TODO: add video_m4v

    # these are downloadable urls
    video_ogv_length = models.IntegerField(null=True)
    video_ogv_url = models.URLField(max_length=255, null=True)
    video_mp4_length = models.IntegerField(null=True)
    video_mp4_url = models.URLField(max_length=255, null=True)
    video_webm_length = models.IntegerField(null=True)
    video_webm_url = models.URLField(max_length=255, null=True)

    # source url in case we need to find things again
    source_url = models.URLField(max_length=255, null=True)

    # whiteboard for editor notes
    whiteboard = models.CharField(max_length=255, blank=True, default=u'')

    # when the video was originally recorded
    recorded = models.DateField(null=True)

    # when the video was added to this site
    added = models.DateTimeField(auto_now_add=True)

    # when the video metadata was last updated
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return '<Video %s (%s)>' % (self.title[:30], self.category)

    class Meta(object):
        get_latest_by = 'recorded'
        ordering = ['-recorded', 'title']

    @models.permalink
    def get_absolute_url(self):
        return ('videos-video', (self.pk, self.slug))

    def save(self):
        self.slug = slugify(self.title[:49])
        super(Video, self).save()

    def get_thumbnail_url(self):
        """Use a local image if it exists, otherwise fall back to the
        remote image url."""
        local_path = self.LOCAL_THUMBNAIL_PATH % self.pk
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, local_path)):
            return os.path.join(settings.MEDIA_URL, local_path)
        else:
            return self.thumbnail_url


class RelatedUrl(models.Model):
    video = models.ForeignKey(Video, related_name='related_urls')
    url = models.URLField(max_length=255)
    description = models.CharField(max_length=255, blank=True, default=u'')

    def __unicode__(self):
        return '<URL %s>' % self.url


def create_speakers(speakers):
    ret = []

    for name in speakers:
        name = name.strip()
        try:
            s = Speaker.objects.get(name=name)
            ret.append(s)
        except (Speaker.DoesNotExist, Speaker.MultipleObjectsReturned):
            s = Speaker(name=name, slug=slugify(name))
            s.save()
            ret.append(s)
    return ret


def create_tags(tags):
    ret = []

    for tag in tags:
        tag = tag.strip()
        try:
            t = Tag.objects.get(tag=tag)
            ret.append(t)
        except Tag.DoesNotExist:
            t = Tag(tag=tag)
            t.save()
            ret.append(t)
    return ret

class BadVideoError(Exception):
    pass


def create_videos(data):
    created = []
    for mem in data:
        if not 'source_url' in mem:
            raise BadVideoError('missing source_url')

        try:
            v = Video.objects.get(source_url=mem['source_url'])
            continue

        except Video.DoesNotExist:
            # Fix category
            cat = Category.objects.get(pk=mem['category'])
            mem['category'] = cat

            # TODO: convert dates from strings here

            # TODO: switch to use .pop()

            # Take out speakers and tags
            speakers = mem.get('speakers', [])
            tags = mem.get('tags', [])

            for badthing in ('tags', 'speakers'):
                if badthing in mem:
                    del mem[badthing]

            v = Video(**mem)
            v.save()

            # Add speakers and tags
            for s in create_speakers(speakers):
                v.speakers.add(s)
            for t in create_tags(tags):
                v.tags.add(t)

            v.save()
            created.append(v)
    return created

