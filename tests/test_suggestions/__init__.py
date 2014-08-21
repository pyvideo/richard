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

import itertools

from ..test_base import with_save
from richard.suggestions.models import Suggestion


_count = itertools.count()


@with_save
def suggestion(**kwargs):
    defaults = {}
    defaults.update(kwargs)

    if 'name' not in defaults:
        defaults['name'] = u'Add pycon conference ' + str(next(_count))
    if 'url' not in defaults:
        defaults['url'] = u'https://us.pycon.org/2012/' + str(next(_count))

    return Suggestion(**defaults)
