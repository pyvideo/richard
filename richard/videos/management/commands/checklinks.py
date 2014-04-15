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


from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
import requests

from richard.videos.models import Video


class Command(BaseCommand):
    args = '[<id id...>]'
    help = 'Check Video URLs for availability'

    states = [state[0] for state in Video.STATE_CHOICES]
    verbose = 0

    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all', default=True,
            help='Check URL availability for all videos.'),
        make_option(
            '-s',
            '--state',
            dest='state',
            type='choice',
            choices=states,
            action='store',
            default=None,
            metavar='STATE',
            help='Check URL availability for videos in the requested state.'
                    + ' Valid choices: %s.' % states,
        ),
    )


    def handle(self, *args, **options):
        self.verbose = int(options.get('verbosity'))
        checked = 0

        if options['all']:
            videos = Video.objects.all()
        elif options['state']:
            videos = Video.objects.filter(state=options['state'])
        elif len(args) > 0:
            videos = Video.objects.filter(id__in=args)
        else:
            raise CommandError('missing required options')

        total = len(videos)

        for ind, v in enumerate(videos):
            self.log('%d/%d: Checking URLs for id %s video %s' % (ind, total, v.id, v.title))
            self.check_video(v)
            checked += 1

        self.log('Checked %d videos\n' % checked)


    def check_video(self, v):
        """ make a HEAD request against all URLFields in a Video

        If something fails, print it out.
        """
        urls = self.all_urls(v)
        for url in urls:
            try:
                r = requests.head(url)
                if not r.ok:
                    self.log('FAIL: status %s video %s URL %s' % (r.status_code, v.id, url))
                self.log('SUCCESSS: video %s URL %s' % (v.id, url))
            except requests.exceptions.RequestException:
                self.log('FAIL: requests call failed for video %s URL %s' % (v.id, url))


    def all_urls(self, video):
        """ returns a list of all the poopulated URLs of this Video
        maybe later we want to be clever and introspect for URLFields?
        """
        return [url for url in
            [
                video.thumbnail_url, video.video_ogv_url, video.video_mp4_url,
                video.video_webm_url, video.video_flv_url,
            ]
            if url is not None
        ]


    def log(self, msg):
        if self.verbose:
            self.stdout.write(msg)
