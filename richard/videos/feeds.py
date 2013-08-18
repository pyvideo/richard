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

from datetime import datetime, time

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.translation import ugettext as _

from richard.videos.models import Speaker, Category, Video


class MediaRSSFeed(Rss201rev2Feed):
    """Implements parts of the Media RSS specification.

    http://www.rssboard.org/media-rss
    """
    def rss_attributes(self):
        attrs = super(MediaRSSFeed, self).rss_attributes()
        attrs[u'xmlns:media'] = u'http://search.yahoo.com/mrss/'
        return attrs

    def add_item_elements(self, handler, item):
        super(MediaRSSFeed, self).add_item_elements(handler, item)

        if 'enclosures' in item and len(item['enclosures']) > 1:
            handler.startElement(u'media:group', {})
            for e in item['enclosures']:
                handler.addQuickElement(u'media:content', '', e)
            handler.endElement(u'media:group')

        if 'keywords' in item:
            handler.addQuickElement(u"media:keywords", item['keywords'])

        for name, attrs in item.get('media', {}).items():
            handler.addQuickElement(u'media:%s' % name, '', attrs)


class CategoryFeed(Feed):
    """Feed of categories"""
    feed_type = Rss201rev2Feed
    ttl = 500
    description_template = 'videos/category_feed_video.html'

    def link(self):
        return reverse('videos-category-feed')

    def title(self):
        return _(u'{site_title}: Categories').format(
            site_title=settings.SITE_TITLE)

    def items(self):
        cats = (Category.objects.filter(video__state=Video.STATE_LIVE)
                                .order_by('-added'))
        return cats[:settings.MAX_FEED_LENGTH]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        if item.start_date:
            return datetime.combine(item.start_date, time())
        else:
            return None

    def item_link(self, item):
        return item.get_absolute_url()


class BaseVideoFeed(Feed):
    feed_type = MediaRSSFeed
    ttl = 500

    # item_categories -- category + tags?
    # item_copyright

    def item_title(self, item):
        return item.title

    def item_description(self, video):
        desc = []
        if video.summary:
            desc.append(u'<p>Abstract</p>')
            desc.append(video.summary)
        if video.description:
            desc.append(u'<p>Description</p>')
            desc.append(video.description)
        return u'\n'.join(desc)

    def item_pubdate(self, video):
        # pubdate needs to be a datetime object, recorded is just a date
        if video.recorded:
            return datetime.combine(video.recorded, time())
        else:
            return None

    def item_link(self, video):
        return video.get_absolute_url()

    def item_author_name(self, video):
        # TODO: This returns a list of authors, but maybe there's
        # a better way to do that with MRSS
        return u','.join([s.name for s in video.speakers.all()])

    # MediaRSS specific

    def item_enclosures(self, item):
        enclosures = []
        for fmt in item.get_feed_formats():
            data = {'url': fmt['url']}
            if fmt.get('mime_type'):
                data['mime_type'] = fmt['mime_type']
            if fmt.get('length'):
                data['fileSize'] = str(fmt['length'])

            enclosures.append(data)
        return enclosures

    def item_media(self, item):
        # TODO no point in including a 'no thumbnail' image
        return {'thumbnail': {'url': item.get_thumbnail_url()}}

    def item_extra_kwargs(self, item):
        # provides us with an API similar to the rest of the Feed class
        return {'enclosures': self.item_enclosures(item),
                'media': self.item_media(item)}

    # RSS enclosure (fallback if MediaRSS is not supported by the client)
    # This uses the first format that is available, according to the
    # MEDIA_PREFERENCE setting.

    def item_enclosure_url(self, item):
        fmt = item.get_feed_formats()
        if fmt:
            return fmt[0]['url']
        else:
            return None

    def item_enclosure_length(self, item):
        fmt = item.get_feed_formats()
        if fmt:
            return fmt[0].get('length')
        else:
            return None

    def item_enclosure_mime_type(self, item):
        fmt = item.get_feed_formats()
        if fmt:
            return fmt[0].get('mime_type')
        else:
            return None


class CategoryVideosFeed(BaseVideoFeed):
    """Videos of a single category, e.g. of a conference."""
    def link(self, category):
        return reverse('videos-category-videos-feed',
                       kwargs={'category_id': category.pk,
                               'slug': category.slug})

    def title(self, category):
        return _(u'{site_title}: Videos of {category}').format(
            site_title=settings.SITE_TITLE, category=category.title)

    def get_object(self, request, category_id, slug):
        return get_object_or_404(Category, pk=category_id)

    def items(self, category):
        return category.video_set.live()


class SpeakerVideosFeed(BaseVideoFeed):
    """Videos of a single speaker."""
    def link(self, speaker):
        return reverse('videos-speaker-feed',
                       kwargs={'speaker_id': speaker.pk, 'slug': speaker.slug})

    def title(self, speaker):
        return _(u'{site_title}: Videos of {speaker}').format(
            site_title=settings.SITE_TITLE, speaker=speaker.name)

    def get_object(self, request, speaker_id, slug):
        return get_object_or_404(Speaker, pk=speaker_id)

    def items(self, speaker):
        return speaker.video_set.live()


class NewPostedVideoFeed(BaseVideoFeed):
    """Feed for newly posted videos."""
    def link(self):
        return reverse('videos-new-feed')

    def title(self):
        return _(u'{site_title}: Newly posted videos').format(
            site_title=settings.SITE_TITLE)

    def items(self):
        videos = Video.objects.live().order_by('-added')
        return videos[:settings.MAX_FEED_LENGTH]
