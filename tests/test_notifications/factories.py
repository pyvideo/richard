# richard -- video index system
# Copyright (C) 2012, 2013, 2014, 2015 richard contributors.  See AUTHORS.
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
import datetime

import factory
from factory import fuzzy
import pytz

from richard.notifications import models


class NotificationFactory(factory.DjangoModelFactory):
    START_DATE = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=14)

    start_date = fuzzy.FuzzyDateTime(start_dt=START_DATE)

    class Meta:
        exclude = ('START_DATE',)
        model = models.Notification
