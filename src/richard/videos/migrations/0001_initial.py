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
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='The complete title for the category. e.g. PyCon 2010', max_length=255)),
                ('description', models.TextField(default='', help_text='Use Markdown', blank=True)),
                ('url', models.URLField(default='', help_text='URL for the category. e.g. If this category was a conference, this would be the url for the conference web-site.', blank=True)),
                ('start_date', models.DateField(help_text='If the category was an event, then this is the start date for the event.', null=True, blank=True)),
                ('whiteboard', models.CharField(default='', help_text='Editor notes for this category.', max_length=255, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso639_1', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255)),
                ('description', models.CharField(default='', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'speaker',
                'verbose_name_plural': 'speakers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['tag'],
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=2, choices=[(1, 'Live'), (2, 'Draft')])),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField(default='', help_text='Use Markdown', blank=True)),
                ('description', models.TextField(default='', help_text='Use Markdown', blank=True)),
                ('quality_notes', models.TextField(default='', blank=True)),
                ('copyright_text', models.TextField(blank=True)),
                ('embed', models.TextField(blank=True)),
                ('thumbnail_url', models.URLField(max_length=255, null=True, blank=True)),
                ('duration', models.IntegerField(help_text=b'In seconds', null=True, blank=True)),
                ('video_ogv_length', models.IntegerField(null=True, blank=True)),
                ('video_ogv_url', models.URLField(max_length=255, null=True, blank=True)),
                ('video_ogv_download_only', models.BooleanField(default=False)),
                ('video_mp4_length', models.IntegerField(null=True, blank=True)),
                ('video_mp4_url', models.URLField(max_length=255, null=True, blank=True)),
                ('video_mp4_download_only', models.BooleanField(default=False)),
                ('video_webm_length', models.IntegerField(null=True, blank=True)),
                ('video_webm_url', models.URLField(max_length=255, null=True, blank=True)),
                ('video_webm_download_only', models.BooleanField(default=False)),
                ('video_flv_length', models.IntegerField(null=True, blank=True)),
                ('video_flv_url', models.URLField(max_length=255, null=True, blank=True)),
                ('video_flv_download_only', models.BooleanField(default=False)),
                ('source_url', models.URLField(max_length=255, null=True, blank=True)),
                ('whiteboard', models.CharField(default='', max_length=255, blank=True)),
                ('recorded', models.DateField(null=True, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(related_name='videos', to='videos.Category')),
                ('language', models.ForeignKey(to='videos.Language', null=True)),
                ('speakers', models.ManyToManyField(related_name='videos', to='videos.Speaker', blank=True)),
                ('tags', models.ManyToManyField(related_name='videos', to='videos.Tag', blank=True)),
            ],
            options={
                'ordering': ['-recorded', 'title'],
                'get_latest_by': 'recorded',
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoUrlStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('check_date', models.DateTimeField()),
                ('status_code', models.IntegerField()),
                ('status_message', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(max_length=255)),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='relatedurl',
            name='video',
            field=models.ForeignKey(related_name='related_urls', to='videos.Video'),
            preserve_default=True,
        ),
    ]
