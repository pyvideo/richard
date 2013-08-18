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
from django import template


register = template.Library()


@register.filter
def duration(duration):
    """Filter that converts a duration in seconds to something like 01:54:01
    """
    if duration is None:
        return ''

    duration = int(duration)
    seconds = duration % 60
    minutes = (duration // 60) % 60
    hours = (duration // 60) // 60

    s = '%02d' % (seconds)
    m = '%02d' % (minutes)
    h = '%02d' % (hours)

    output = []
    if hours > 0:
        output.append(h)
    output.append(m)
    output.append(s)
    return ':'.join(output)
