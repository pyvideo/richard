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
from collections import namedtuple


Browser = namedtuple(
    'Browser', [
        'name', 'version', 'platform_version', 'mobile', 'tablet'])


def parse_ua(ua):
    # TODO: Flesh this out--it's ultra-basic and barely meets my
    # needs.
    data = {
        'name': '',
        'version': None,
        'platform_version': '',
        'mobile': False,
        'tablet': False
        }

    ua = ua.lower()
    if 'firefox' in ua:
        data['name'] = 'Firefox'

    if 'mobile' in ua:
        data['mobile'] = True
    elif 'tablet' in ua:
        data['tablet'] = True

    return Browser(**data)


class BrowserDetectMiddleware(object):
    """
    Detects browser bits from the UA and flags the request
    accordingly.
    """
    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        request.BROWSER = parse_ua(ua)
