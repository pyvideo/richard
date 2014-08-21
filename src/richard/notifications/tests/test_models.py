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

from datetime import datetime, timedelta

from django.test import TestCase
from nose.tools import eq_

from richard.notifications.tests import notification
from richard.notifications.models import Notification


class TestNotification(TestCase):

    def test_shown(self):
        """
        Test that notifications where now is between their start and end
        date are returned.
        """
        start = datetime.now() - timedelta(days=2)
        end = datetime.now() + timedelta(days=2)
        n1 = notification(start_date=start, end_date=end, save=True)

        start -= timedelta(days=1)
        n2 = notification(start_date=start, end_date=end, save=True)

        n3 = notification(start_date=start, save=True)

        eq_([x.pk for x in Notification.objects.get_live_notifications()],
            [n1.pk, n2.pk, n3.pk])

    def test_not_shown(self):
        """
        Test that notifications where now is before their start date or after
        their end date are not returned.
        """
        start = datetime.now() + timedelta(days=2)
        end = datetime.now() + timedelta(days=3)
        notification(start_date=start, end_date=end, save=True)

        start = datetime.now() - timedelta(days=2)
        end = datetime.now() - timedelta(days=1)
        notification(start_date=start, end_date=end, save=True)

        eq_(len(Notification.objects.get_live_notifications()), 0)
