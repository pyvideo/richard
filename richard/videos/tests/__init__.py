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

import uuid

from django.utils.six import text_type
from django.utils.text import slugify

from richard.videos.models import (
    Category, Speaker, Tag, Video, RelatedUrl, Language)
from richard.base.tests import with_save


@with_save
def category(**kwargs):
    defaults = {}
    defaults.update(kwargs)

    if 'title' not in defaults:
        defaults['title'] = text_type(uuid.uuid4()) + u' 2012'
    if 'slug' not in defaults:
        defaults['slug'] = slugify(text_type(defaults['title']))

    return Category(**defaults)


@with_save
def language(**kwargs):
    defaults = {
        'iso639_1': 'en',
        'name': 'English'
        }
    defaults.update(kwargs)
    return Language(**defaults)


@with_save
def speaker(**kwargs):
    defaults = {
        'name': u'Ben Guaraldi'
        }
    defaults.update(kwargs)

    if 'slug' not in defaults:
        defaults['slug'] = slugify(text_type(defaults['name']))

    return Speaker(**defaults)


@with_save
def tag(**kwargs):
    defaults = {
        'tag': u'tagless'
        }
    defaults.update(kwargs)

    return Tag(**defaults)


@with_save
def related_url(**kwargs):
    return RelatedUrl(**kwargs)


@with_save
def video(**kwargs):
    defaults = {
        'title': 'How to build a video index site in 3 weeks',
        }
    defaults.update(kwargs)

    if 'category' not in defaults:
        cat = category()
        cat.save()
        defaults['category'] = cat

    return Video(**defaults)
