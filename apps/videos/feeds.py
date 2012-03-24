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

from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from videos.models import Video


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

        if 'enclosures' in item:
            group = len(item['enclosures']) > 1
            if group:
                handler.startElement(u'media:group', {})

            for e in item['enclosures']:
                data = {u'url': e['url']}
                handler.addQuickElement(u'media:content', '', data)

            if group:
                handler.endElement(u'media:group')

        if 'title' in item:
            handler.addQuickElement(u'media:title', item['title'])
        if 'description' in item:
            handler.addQuickElement(u'media:description', item['description'])
        if 'keywords' in item:
            handler.addQuickElement(u"media:keywords", item['keywords'])

        for name, attrs in item.get('media', []).items():
            handler.addQuickElement(u'media:%s' % name, '', attrs)


class VideoFeed(Feed):
    feed_type = MediaRSSFeed
    title = "Videos"
    description = "Updates on changes and additions to SITE."
    ttl = 500

    def link(self, obj):
        return reverse('videos-feed')

    # item_categories -- category + tags?
    # item_copyright

    def items(self):
        return Video.objects.live()[:10]

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
        # TODO the Video model should tell us what sources are available
        sources = ('source', 'video_ogv', 'video_mp4', 'video_webm', )
        enclosures = []

        for source in sources:
            field = source + '_url'
            if getattr(item, field):
                enclosures.append({'url': getattr(item, field)})

        return enclosures

    def item_media(self, item):
        # TODO no point in including a 'no thumbnail' image
        return {'thumbnail': {'url': item.get_thumbnail_url()}}

    def item_extra_kwargs(self, item):
        # provides us with an API similar to the rest of the Feed class
        return {'enclosures': self.item_enclosures(item),
                'media': self.item_media(item)}
