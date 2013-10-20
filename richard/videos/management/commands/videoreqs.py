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

import json

from django.db.models import fields
from django.core.management.base import BaseCommand

from richard.videos.models import Video


class Command(BaseCommand):
    help = 'Generates a JSON file with requirements for video'

    def handle(self, *args, **options):
        # Generate the basic stuff
        reqs = []
        for field in Video._meta.fields:
            # Skip some things that shouldn't be in an API push
            if field.name in ['id', 'updated', 'added']:
                continue

            data = {
                'name': field.name,
                'type': field.get_internal_type(),
                'has_default': field.default is not fields.NOT_PROVIDED,
                'null': field.null,
                'empty_strings': field.empty_strings_allowed,
                'md': 'markdown' in field.help_text.lower(),
                'choices': [mem[0] for mem in field.choices]
                }

            if field.name == 'category':
                data.update({
                        'type': 'TextField',
                        'empty_strings': False,
                        'null': False,
                        'has_default': False,
                        'md': False,
                        'choices': []
                        })
            elif field.name == 'language':
                data.update({
                        'type': 'TextField',
                        'empty_strings': False,
                        'null': False,
                        'has_default': False,
                        'md': False,
                        'choices': []
                        })

            reqs.append(data)

        # Add tags and speakers which are M2M, but we do them funkily
        # in the API.
        reqs.append({
                'name': 'tags',
                'type': 'TextArrayField',
                'empty_strings': False,
                'null': True,
                'has_default': False,
                'md': False,
                'choices': []
                })
        reqs.append({
                'name': 'speakers',
                'type': 'TextArrayField',
                'empty_strings': False,
                'has_default': False,
                'null': True,
                'md': False,
                'choices': []
                })

        f = open('video_reqs.json', 'w')
        f.write(json.dumps(reqs, indent=2))
        f.close()

        self.stdout.write('Done!\n')
