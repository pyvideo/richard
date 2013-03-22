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

from django.conf import settings

from jinja2 import Markup
from jingo import register
import markdown

from sitenews import models


def base(request):
    """Adds basic things to the context"""
    notifications = models.Notification.get_live_notifications()

    return {
        'settings': settings,
        'notifications': notifications
        }


@register.function
def page_title(s=None):
    """Function that generates the page title."""
    if s is None:
        return settings.SITE_TITLE
    if len(s) > 80:
        s = s[:80] + u'...'
    return u'%s - %s' % (settings.SITE_TITLE, s)


@register.filter
def md(text):
    """Filter that converts Markdown text -> HTML."""
    return Markup(markdown.markdown(
            text,
            output_format='html5',
            safe_mode='replace',
            html_replacement_text='[HTML REMOVED]'))


@register.filter
def duration(duration):
    """Filter that converts a duration in seconds to
    something like 01:54:01"""

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
