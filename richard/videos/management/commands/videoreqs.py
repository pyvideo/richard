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

import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from richard.videos.models import Video


class Command(BaseCommand):
    help = 'Generates a JSON file with requirements for video'

    def handle(self, *args, **options):
        verbose = int(options.get('verbosity'))

        # Generate the basic stuff
        fields = {}
        for field in Video._meta.fields:
            if field.name == 'id':
                continue

            fields[field.name] = {
                'type': field.get_internal_type(),
                'null': field.null,
                'empty_strings': field.empty_strings_allowed,
                'choices': [mem[0] for mem in field.choices],
                'html': 'html' in field.help_text.lower()
                }

        # Remove the icky things
        for key in ['id', 'updated']:
            if key in fields:
                del fields[key]

        # Fix the things that are slightly different in the API
        fields['category'] = {
            'type': 'TextField',
            'empty_strings': False,
            'null': False,
            'choices': [],
            'html': False
            }
        fields['language'] = {
            'type': 'TextField',
            'empty_strings': False,
            'null': False,
            'choices': [],
            'html': False
            }
        fields['tags'] = {
            'type': 'TextArrayField',
            'empty_strings': False,
            'null': False,
            'choices': [],
            'html': False
            }
        fields['speakers'] = {
            'type': 'TextArrayField',
            'empty_strings': False,
            'null': False,
            'choices': [],
            'html': False
            }

        f = open('video_reqs.json', 'w')
        f.write(json.dumps(fields, indent=2))
        f.close()

        self.stdout.write('Done!\n')

