import unittest
from richard.context_processors import duration


class DurationFilterTest(unittest.TestCase):

    def test_seconds(self):
        self.assertEquals("00:15", duration('15'))
        self.assertEquals("00:01", duration('1'))

    def test_minutes(self):
        self.assertEquals("01:01", duration('61'))
        self.assertEquals("01:00", duration('60'))
        self.assertEquals("02:00", duration('120'))

    def test_hours(self):
        self.assertEquals("01:00:00", duration('3600'))
        self.assertEquals("01:00:02", duration('3602'))
        self.assertEquals("02:00:00", duration('7200'))
        self.assertEquals("02:02:00", duration('7320'))
        self.assertEquals("02:02:01", duration('7321'))
        self.assertEquals("02:02:02", duration('7322'))
