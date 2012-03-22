# richard -- video index system
# Copyright (C) 2012 richard contributors.  See AUTHORS.
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

from functools import wraps
from django.test import TestCase
from nose.tools import eq_


def with_save(func):
    """
    Decorates the given modelmaker adding the `save` keyword argument.

    If save is provided and its `True`, the created model will be
    saved after its creation.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        save = kwargs.pop('save', False)

        model = func(*args, **kwargs)

        if save and callable(getattr(model, 'save', None)):
            model.save()

        return model
    
    return wrapper


class ViewTestCase(TestCase):
    """Helper class for testing views."""

    def _assert_get_HTTP(self, url, data, status_code):
        """Assert that the given URL returns `status_code` HTTP code."""
        data = data if data is not None else {}

        response = self.client.get(url, data)
        eq_(response.status_code, status_code)

    def assert_HTTP_200(self, url, data=None):
        """
        Assert that the given URL returns a 200 HTTP code
        whit a GET request.
        
        Optionally, a dict with arguments for the request can be
        given.
        """
        self._assert_get_HTTP(url, data, 200)

    def assert_HTTP_404(self, url, data=None):
        """
        Assert that the given URL returns a 404 HTTP code
        whit a GET request.
        
        Optionally, a dict with arguments for the request can be
        given.
        """
        self._assert_get_HTTP(url, data, 404)

    def assert_used_templates(self, url, data=None, templates=None):
        """
        Assert that every template in ``templates`` list was rendered 
        after hitting ``url``.
        """
        data = data if data is not None else {}
        if templates is None:
            return

        response = self.client.get(url)
        for template in templates:
            self.assertTemplateUsed(response, template)

    def assert_contains(self, url , data=None, text=''):
        """
        Assert that requesting the given URL with `data` as GET parameters
        contains `text`.
        """
        data = data if data is not None else {}

        response = self.client.get(url, data)
        self.assertContains(response, text)
