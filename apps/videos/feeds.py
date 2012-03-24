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

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed


class BaseVideoFeed(Feed):
    """Base feed for MRSS-supprting feeds holding videos"""
    feed_type = Rss201rev2Feed

    title_template = None
    description_template = None

    def root_attributes(self):
        attrs = super(BaseVideoFeed, self).root_attributes()
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        return attrs

    def ttl(self):
        return u'500'

    def item_title(self, video):
        return video.summary

    def item_description(self, video):
        desc = []
        if video.summary:
            desc.append(u'<p>Abstract</p>')
            desc.append(video.summary)
        if video.description:
            desc.append(u'<p>Description</p>')
            desc.append(video.description)
        return u'\n'.join(desc)

    def item_link(self, video):
        return video.get_absolute_url()

    def item_author_name(self, video):
        # TODO: This returns a list of authors, but maybe there's
        # a better way to do that with MRSS
        return u','.join([s.name for s in video.speakers.all()])

    # item_enclosure_url
    # item_enclosure_length (in bytes)
    # item_enclosure_mime_type
    
    def item_pubdate(self, video):
        return video.recorded

    # item_categories -- category + tags?
    # item_copyright

    def add_item_elements(self, handler, video):
        super(BaseVideoFeed, self).add_item_elements(handler, item)

        if 'media:title' in item:
            handler.addQuickElement(u"media:title", item['title'])
        if 'media:description' in item:
            handler.addQuickElement(u"media:description", item['description'])

        if 'content_url' in item:
            content = dict(url=item['content_url'])
            if 'content_width' in item:
                content['width'] = str(item['content_width'])
            if 'content_height' in item:
                content['height'] = str(item['content_height'])
            handler.addQuickElement(u"media:content", '', content)
        
        if 'thumbnail_url' in item:
            thumbnail = dict(url=item['thumbnail_url'])
            if 'thumbnail_width' in item:
                thumbnail['width'] = str(item['thumbnail_width'])
            if 'thumbnail_height' in item:
                thumbnail['height'] = str(item['thumbnail_height'])
            handler.addQuickElement(u"media:thumbnail", '', thumbnail)

        if 'keywords' in item:
            handler.addQuickElement(u"media:keywords", item['keywords'])
