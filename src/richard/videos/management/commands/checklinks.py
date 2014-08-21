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


from collections import Counter
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from richard.videos.models import Video, VideoUrlStatus


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
        status_counter = Counter()

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
            self.log('%d/%d: Checking URLs for id %s video %s' % (ind, total, v.id, v.title), min_verbose=2)
            ret = VideoUrlStatus.objects.create_for_video(v)
            if ret:
                self.log('       %s' % unicode(ret), min_verbose=2)
            status_counter += ret
            checked += 1
        self.log('Checked %d videos\n' % checked)
        self.log(unicode(status_counter))

    def log(self, msg, min_verbose=1):
        if self.verbose >= min_verbose:
            self.stdout.write(msg)
