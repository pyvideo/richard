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

import cStringIO
import os
import urllib

import Image
from django.conf import settings
from django.core.management.base import BaseCommand

from videos.models import Video

THUMBNAIL_SIZE = (160, 120)

class Command(BaseCommand):
    help = 'Fetch thumbnails of all videos and store them locally'

    def handle(self, *args, **options):
        fetched = 0
        videos = Video.objects.exclude(thumbnail_url='')
        for v in videos:
            # Don't overwrite existing thumbnails
            path = Video.LOCAL_THUMBNAIL_PATH % v.pk
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
                continue

            f = urllib.urlopen(v.thumbnail_url)
            data = cStringIO.StringIO(f.read())

            image = Image.open(data)
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(os.path.join(settings.MEDIA_ROOT, path))
            del image
            fetched += 1

        self.stdout.write('Fetched %s images\n' % fetched)
