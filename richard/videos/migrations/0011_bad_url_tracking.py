# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoUrlStatus'
        db.create_table(u'videos_videourlstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('check_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('status_code', self.gf('django.db.models.fields.IntegerField')()),
            ('status_message', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videos.Video'])),
        ))
        db.send_create_signal(u'videos', ['VideoUrlStatus'])


    def backwards(self, orm):
        # Deleting model 'VideoUrlStatus'
        db.delete_table(u'videos_videourlstatus')


    models = {
        u'videos.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        u'videos.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso639_1': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'videos.relatedurl': {
            'Meta': {'object_name': 'RelatedUrl'},
            'description': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_urls'", 'to': u"orm['videos.Video']"})
        },
        u'videos.speaker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speaker'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'videos.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'videos.video': {
            'Meta': {'ordering': "['-recorded', 'title']", 'object_name': 'Video'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['videos.Category']"}),
            'copyright_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'embed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['videos.Language']", 'null': 'True'}),
            'quality_notes': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['videos.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['videos.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'video_flv_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_flv_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_flv_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_mp4_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_mp4_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_mp4_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_ogv_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_ogv_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_ogv_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_webm_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_webm_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_webm_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        u'videos.videourlstatus': {
            'Meta': {'object_name': 'VideoUrlStatus'},
            'check_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['videos.Video']"})
        }
    }

    complete_apps = ['videos']