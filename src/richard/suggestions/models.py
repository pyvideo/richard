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

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Suggestion(models.Model):
    """Represents a suggestion for videos to be added to the site."""

    STATE_NEW = 0
    STATE_IN_PROGRESS = 1
    STATE_COMPLETED = 2
    STATE_REJECTED = 3
    STATE_SPAM = 4

    RESOLVED_STATES = (STATE_COMPLETED, STATE_REJECTED)
    OPEN_STATES = (STATE_NEW, STATE_IN_PROGRESS)

    STATE_CHOICES = (
        (STATE_NEW, _(u'New')),
        (STATE_IN_PROGRESS, _(u'In progress')),
        (STATE_COMPLETED, _(u'Completed')),
        (STATE_REJECTED, _(u'Rejected')),
        (STATE_SPAM, _(u'Spam')),
        )

    state = models.IntegerField(choices=STATE_CHOICES, default=STATE_NEW)

    name = models.CharField(
        max_length=128,
        help_text=_(u'Name of video/collection of videos'),
        unique=True)
    url = models.URLField(
        max_length=255,
        help_text=_(u'Link to video/collection of videos'),
        unique=True)
    comment = models.TextField(
        blank=True,
        help_text=_(u'Additional information, urls, etc (optional)'))

    whiteboard = models.CharField(
        max_length=255, blank=True, default=u'',
        help_text=_(u'Editor notes for this suggestion.'))
    resolution = models.CharField(
        max_length=128, blank=True, default=u'',
        help_text=_(u'Describe how this suggestion was resolved.'))

    submitted = models.DateTimeField(auto_now_add=True)
    resolved = models.DateTimeField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = _(u'suggestion')
        verbose_name_plural = _(u'suggestions')

    def save(self, *args, **kwargs):
        """When the suggestion is closed, set the resolved date."""
        if self.state in Suggestion.RESOLVED_STATES:
            self.resolved = datetime.now()
        else:
            # Reset resolved date when the suggestion is reopened
            self.resolved = None

        super(Suggestion, self).save(*args, **kwargs)
