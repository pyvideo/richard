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

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist


def pages_view(request, page):
    """Show a simple page.

    Only pages that are defined in the PAGES setting will be shown, otherwise
    return a 404.
    """
    if page in settings.PAGES:
        try:
            return render(request, 'pages/%s.html' % page, {})
        except TemplateDoesNotExist:
            # there is no template for this page, raise a 404 below
            pass

    raise Http404
