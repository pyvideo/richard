# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Suggestion'
        db.create_table('suggestions_suggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('whiteboard', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('resolved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('suggestions', ['Suggestion'])

    def backwards(self, orm):
        # Deleting model 'Suggestion'
        db.delete_table('suggestions_suggestion')

    models = {
        'suggestions.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resolution': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
            'resolved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['suggestions']