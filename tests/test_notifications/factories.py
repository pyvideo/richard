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
