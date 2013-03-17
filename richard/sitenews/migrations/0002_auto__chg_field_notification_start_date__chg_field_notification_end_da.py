# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Get the data and put it in memory (this seems dumb, but it's
        # probably fine at this point in time since it's unlikely
        # anyone is running richard.
        lookup_dates = []
        if not db.dry_run:
            for notification in orm.Notification.objects.all():
                lookup_dates.append(
                    (notification.id, notification.start_date, notification.end_date))

        # Alter the columns
        db.alter_column('sitenews_notification', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))
        db.alter_column('sitenews_notification', 'end_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Wipe those columns.
        if not db.dry_run:
            db.execute('UPDATE sitenews_notification SET start_date = null')
            db.execute('UPDATE sitenews_notification SET end_date = null')

        # Alter the columns
        db.alter_column('sitenews_notification', 'start_date', self.gf('django.db.models.fields.DateField')(null=True))
        db.alter_column('sitenews_notification', 'end_date', self.gf('django.db.models.fields.DateField')(null=True))

        if not db.dry_run:
            # Go through the stuff we stuck in a hashmap and save it.
            for id_, start_date, end_date in lookup_dates:
                db.execute(
                    'UPDATE sitenews_notification SET start_date = %s, end_date = %s WHERE id = %s',
                    ['{}-{}-{}'.format(start_date.year, start_date.month, start_date.day),
                     '{}-{}-{}'.format(end_date.year, end_date.month, end_date.day),
                    id_])

        # Alter the columns
        db.alter_column('sitenews_notification', 'start_date', self.gf('django.db.models.fields.DateField')())
        db.alter_column('sitenews_notification', 'end_date', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        if not db.dry_run:
            raise RuntimeError("Cannot reverse this migration.")


    models = {
        'sitenews.notification': {
            'Meta': {'object_name': 'Notification'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interjection': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sitenews.sitenews': {
            'Meta': {'ordering': "['-created']", 'object_name': 'SiteNews'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sitenews']
