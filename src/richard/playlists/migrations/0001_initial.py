# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', models.CharField(help_text=b'Summary of the playlist', max_length=100)),
                ('description', models.TextField(default='', help_text=b'Long description of the playlist (in markdown).', blank=True)),
                ('data', models.CommaSeparatedIntegerField(help_text=b'Comma-separated list of video ids for this playlist.', max_length=255, blank=True)),
                ('updated', models.DateTimeField(help_text=b'Last time this playlist was updated.', auto_now=True)),
                ('user', models.ForeignKey(help_text=b'User that owns this playlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['summary'],
            },
            bases=(models.Model,),
        ),
    ]
