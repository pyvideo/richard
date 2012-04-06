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

import uuid

from django.template.defaultfilters import slugify

from videos.models import CategoryKind, Category, Speaker, Tag, Video
from richard.tests.utils import with_save


def category_kind(**kwargs):
    defaults = {
        'name': 'foo'
        }
    defaults.update(kwargs)

    return CategoryKind(**defaults)


@with_save
def category(**kwargs):
    defaults = {}
    defaults.update(kwargs)

    if 'name' not in defaults:
        defaults['name'] = str(uuid.uuid4())
    if 'title' not in defaults:
        defaults['title'] = defaults['name'] + u' 2012'
    if 'slug' not in defaults:
        defaults['slug'] = slugify(defaults['name'])
    if 'kind' not in defaults:
        ck = category_kind()
        ck.save()
        defaults['kind'] = ck

    return Category(**defaults)


@with_save
def speaker(**kwargs):
    defaults = {
        'name': 'Ben Guaraldi'
        }
    defaults.update(kwargs)

    if 'slug' not in defaults:
        defaults['slug'] = slugify(defaults['name'])

    return Speaker(**defaults)


@with_save
def tag(**kwargs):
    defaults = {
        'tag': 'tagless'
        }
    defaults.update(kwargs)

    return Tag(**defaults)


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
