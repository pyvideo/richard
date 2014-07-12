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

def seconds_to_hms(duration):
    """Convert seconds to hours, minutes, seconds.
    Represents times over one day as hours > 24.
    """
    duration = int(duration)
    hours, _t = divmod(duration, 3600)
    minutes, seconds = divmod(_t, 60)
    return hours, minutes, seconds


@register.filter
def duration(duration):
    """Filter that converts a duration in seconds to something like 01:54:01
    """
    if duration is None:
        return ''

    hours, minutes, seconds = seconds_to_hms(duration)

    s = '%02d' % (seconds)
    m = '%02d' % (minutes)
    h = '%02d' % (hours)

    output = []
    if hours > 0:
        output.append(h)
    output.append(m)
    output.append(s)
    return ':'.join(output)


@register.filter
def duration_iso8601(duration):
    """Filter that converts a duration in seconds to ISO8601 duration format
    like T01H01M01S. Represents times over one day as hours > 24.
    """
    if not duration:
        hours = minutes = seconds = 0
    else:
        hours, minutes, seconds = seconds_to_hms(duration)
    return 'PT%02dH%02dM%02dS' % (hours, minutes, seconds)

