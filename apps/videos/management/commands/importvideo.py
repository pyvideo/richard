import os
import json
from django.core.management.base import BaseCommand, CommandError
from videos.models import create_videos


class Command(BaseCommand):
    args = '<json-file>'
    help = 'Import video from a json file.'


    def handle(self, *args, **options):
        if not args:
            raise CommandError('Please specify a json file.')

        fn = args[0]

        fn = os.path.abspath(fn)
        if not os.path.exists(fn):
            raise CommandError('"%s" does not exist' % fn)

        f = open(fn, 'r')
        data = json.loads(f.read())
        f.close()
        create_videos(data)
