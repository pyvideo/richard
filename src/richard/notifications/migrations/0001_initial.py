# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interjection', models.CharField(help_text='Short interjection like "Alert!", "Information!", "Warning!", "Heads up!", "Whoops!"', max_length=20)),
                ('text', models.CharField(help_text='Use Markdown. Keep the text short. Add a link to sitenews for more information.', max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
            bases=(models.Model,),
        ),
    ]
