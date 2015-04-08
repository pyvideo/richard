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

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase as DjangoTestCase

from django_browserid.tests import mock_browserid
import factory

from richard.base.models import Profile


class RichardTestCase(DjangoTestCase):
    def client_login_user(self, user):
        with mock_browserid(user.email):
            ret = self.client.login(audience='faux', assertion='faux')
            assert ret, "Login failed."

    def setUp(self):
        super(RichardTestCase, self).setUp()
        cache.clear()

    def tearDown(self):
        super(RichardTestCase, self).tearDown()
        cache.clear()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    # We pass in profile=None to prevent UserFactory from creating
    # another profile (this disables the RelatedFactory)
    user = factory.SubFactory('tests.UserFactory', profile=None)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_%d' % n)
    email = factory.Sequence(lambda n: 'joe%d@example.com' % n)

    # We pass in 'user' to link the generated Profile to our
    # just-generated User This will call
    # ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory(ProfileFactory, 'user')
