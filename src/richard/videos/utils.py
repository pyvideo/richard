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

from django.utils.six import text_type
from django.utils.text import slugify


def generate_unique_slug(obj, slug_from, slug_field='slug'):
    text = getattr(obj, slug_from)[:49]
    root_text = text
    for i in range(100):
        slug = slugify(text_type(text))
        try:
            d = {slug_field: slug}
            obj.__class__.objects.get(**d)
        except obj.__class__.DoesNotExist:
            return slug

        ending = u'-%s' % i
        text = root_text + ending

    raise ValueError('No valid slugs available.')

