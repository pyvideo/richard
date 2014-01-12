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

from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime


class NotificationManager(models.Manager):
    def get_live_notifications(self):
        """Returns notifications in the "now" range

        This is anything that starts before now and either ends after now or
        had a null end date.

        """
        now = datetime.date.today()
        return (
            self.get_query_set()
            .filter(start_date__lte=now)
            .filter(
                models.Q(end_date__gt=now) | models.Q(end_date__isnull=True))
        )


class Notification(models.Model):
    """
    Allows you to add site-wide notifications which appear in a
    notification bubble at the top of every page.
    """
    interjection = models.CharField(
        max_length=20,
        help_text=_(u'Short interjection like "Alert!", "Information!", '
                    u'"Warning!", "Heads up!", "Whoops!"'))

    text = models.CharField(
        max_length=200,
        help_text=_(u'Use Markdown. Keep the text short. Add a link to '
                    u'sitenews for more information.'))

    start_date = models.DateField()
    end_date = models.DateField(null=True)

    objects = NotificationManager()

    class Meta(object):
        verbose_name = _(u'notification')
        verbose_name_plural = _(u'notifications')
