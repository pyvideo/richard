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

import StringIO
import os
from optparse import make_option

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from videos.models import Video


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--overwrite', action='store_true', dest='overwrite',
                    default=False,
                    help='Overwrite existing thumbnails.'),
    )
    help = 'Fetch thumbnails of all videos and store them locally'

    def handle(self, *args, **options):
        verbose = int(options.get('verbosity'))

        # Make PIL only a dependency for this command, not the rest of
        # richard
        try:
            from PIL import Image
        except ImportError:
            raise CommandError('PIL is required for this command.')

        root = os.path.join(settings.MEDIA_ROOT, Video.LOCAL_THUMBNAIL_PATH)
        root = os.path.dirname(root)
        if not os.path.exists(root):
            os.mkdir(root)

        fetched = 0
        videos = Video.objects.exclude(thumbnail_url='')
        total = len(videos)

        for ind, v in enumerate(videos):
            # Don't overwrite existing thumbnails unless we were told so
            path = Video.LOCAL_THUMBNAIL_PATH % v.pk
            if ((not options.get('overwrite') and
                 os.path.exists(os.path.join(settings.MEDIA_ROOT, path)))):
                if verbose:
                    self.stdout.write('%d/%d: Skipping %s (%s)\n' % (
                            ind, total, path, v.title))
                continue

            if verbose:
                self.stdout.write('%d/%d: Fetching %s (%s)\n' % (
                        ind, total, path, v.title))

            res = requests.get(v.thumbnail_url)
            data = StringIO.StringIO(res.content)

            image = Image.open(data)
            image.thumbnail(settings.VIDEO_THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(os.path.join(settings.MEDIA_ROOT, path))
            del image
            fetched += 1

        if verbose:
            self.stdout.write('Fetched %d images\n' % fetched)
