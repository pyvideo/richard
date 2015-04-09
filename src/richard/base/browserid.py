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
from __future__ import print_function
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.http import HttpResponseRedirect

from django_browserid.views import Verify
from django.core.urlresolvers import reverse

from richard.base.models import Profile


class RichardVerify(Verify):
    def login_success(self):
        """Send to new_user view if new user, otherwise send on their way"""
        # Note: This has the side-effect of logging the user in.
        response = super(RichardVerify, self).login_success()

        # If this user has never logged in before, send them to our
        # super secret "Welcome!" page.
        try:
            self.user.profile
            return response

        except Profile.DoesNotExist:
            pass

        url = reverse('new_user')

        redirect_to = self.request.GET.get('next')

        # Do not accept redirect URLs pointing to a different host.
        if redirect_to:
            netloc = urlparse(redirect_to).netloc
            if netloc and netloc != self.request.get_host():
                redirect_to = None

        if redirect_to:
            url = url + '?next=' + redirect_to

        return HttpResponseRedirect(url)
