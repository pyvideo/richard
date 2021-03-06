#!/usr/bin/env python

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

import os
import sys


if __name__ == "__main__":
    # Richard allows overriding of templates and settings and such. To
    # simplify that, we look at the SITE_PATH environment variable for
    # extending the sys.path so things get picked up correctly.
    site_path = os.getenv('SITE_PATH', '')
    if site_path:
        site_path = site_path.split(',')
        sys.path.extend(site_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "richard.config.settings")
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
