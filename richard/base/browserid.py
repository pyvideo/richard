from __future__ import print_function
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.http import HttpResponseRedirect

from django_browserid.views import Verify
from funfactory.urlresolvers import reverse

from fjord.base.models import Profile


class RichardVerify(Verify):
    def login_success(self):
        """Send to new_user view if new user, otherwise send on their way"""
        response = super(RichardVerify, self).login_success()
        # If this user has never logged in before, send them to our
        # super secret "Welcome!" page.
        try:
            self.user.profile
            return response

        except Profile.DoesNotExist:
            url = reverse('new_user')

            redirect_to = self.request.REQUEST.get('next')

            # Do not accept redirect URLs pointing to a different host.
            if redirect_to:
                netloc = urlparse(redirect_to).netloc
                if netloc and netloc != self.request.get_host():
                    redirect_to = None

            if redirect_to:
                url = url + '?next=' + redirect_to

            return HttpResponseRedirect(url)
