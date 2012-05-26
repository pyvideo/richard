# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteNews'
        db.create_table('sitenews_sitenews', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('sitenews', ['SiteNews'])

        # Adding model 'Notification'
        db.create_table('sitenews_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interjection', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sitenews', ['Notification'])

    def backwards(self, orm):
        # Deleting model 'SiteNews'
        db.delete_table('sitenews_sitenews')

        # Deleting model 'Notification'
        db.delete_table('sitenews_notification')

    models = {
        'sitenews.notification': {
            'Meta': {'object_name': 'Notification'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interjection': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sitenews.sitenews': {
            'Meta': {'ordering': "['-updated']", 'object_name': 'SiteNews'},
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