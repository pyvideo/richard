# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CategoryKind'
        db.delete_table('videos_categorykind')

        # Deleting field 'Category.kind'
        db.delete_column('videos_category', 'kind_id')

        # Deleting field 'Category.name'
        db.delete_column('videos_category', 'name')


    def backwards(self, orm):
        # User chose to not deal with backwards NULL issues for
        # 'Category.kind' and 'Category.name'
        raise RuntimeError("Cannot reverse this migration. 'Category.kind' "
                           "and 'Category.name' and its values cannot be restored.")

    models = {
        'videos.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        'videos.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso639_1': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'videos.relatedurl': {
            'Meta': {'object_name': 'RelatedUrl'},
            'description': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_urls'", 'to': "orm['videos.Video']"})
        },
        'videos.speaker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speaker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'videos.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'videos.video': {
            'Meta': {'ordering': "['-recorded', 'title']", 'object_name': 'Video'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Category']"}),
            'copyright_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Language']", 'null': 'True'}),
            'quality_notes': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['videos.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['videos.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['videos']
