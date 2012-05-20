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

from django.db import transaction
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.utils.importlib import import_module


class Command(NoArgsCommand):
    help = 'Load sample data from all installed applications.'

    def handle(self, *args, **options):
        for app_name in settings.INSTALLED_APPS:
            try:
                mod = import_module('%s.sampledata' % app_name)
                if hasattr(mod, 'run'):
                    print "Loading sample data for %s..." % app_name
                    with transaction.commit_on_success():
                        mod.run()
            except ImportError:
                pass # No sampledata module
        print "Done!"
