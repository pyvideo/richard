# -*- coding: utf-8 -*-

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
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0, choices=[(0, 'New'), (1, 'In progress'), (2, 'Completed'), (3, 'Rejected'), (4, 'Spam')])),
                ('name', models.CharField(help_text='Name of video/collection of videos', unique=True, max_length=128)),
                ('url', models.URLField(help_text='Link to video/collection of videos', unique=True, max_length=255)),
                ('comment', models.TextField(help_text='Additional information, urls, etc (optional)', blank=True)),
                ('whiteboard', models.CharField(default='', help_text='Editor notes for this suggestion.', max_length=255, blank=True)),
                ('resolution', models.CharField(default='', help_text='Describe how this suggestion was resolved.', max_length=128, blank=True)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('resolved', models.DateTimeField(null=True, blank=True)),
                ('is_reviewed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'suggestion',
                'verbose_name_plural': 'suggestions',
            },
            bases=(models.Model,),
        ),
    ]
