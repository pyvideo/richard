# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryKind'
        db.create_table('videos_categorykind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('videos', ['CategoryKind'])

        # Adding model 'Category'
        db.create_table('videos_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videos.CategoryKind'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default=u'', max_length=200, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('whiteboard', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('videos', ['Category'])

        # Adding model 'Speaker'
        db.create_table('videos_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('videos', ['Speaker'])

        # Adding model 'Tag'
        db.create_table('videos_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('videos', ['Tag'])

        # Adding model 'Video'
        db.create_table('videos_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videos.Category'])),
            ('quality_notes', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('copyright_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('embed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('video_ogv_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_ogv_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('video_mp4_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_mp4_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('video_webm_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_webm_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('whiteboard', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('recorded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('videos', ['Video'])

        # Adding M2M table for field tags on 'Video'
        db.create_table('videos_video_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm['videos.video'], null=False)),
            ('tag', models.ForeignKey(orm['videos.tag'], null=False))
        ))
        db.create_unique('videos_video_tags', ['video_id', 'tag_id'])

        # Adding M2M table for field speakers on 'Video'
        db.create_table('videos_video_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm['videos.video'], null=False)),
            ('speaker', models.ForeignKey(orm['videos.speaker'], null=False))
        ))
        db.create_unique('videos_video_speakers', ['video_id', 'speaker_id'])

        # Adding model 'RelatedUrl'
        db.create_table('videos_relatedurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_urls', to=orm['videos.Video'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
        ))
        db.send_create_signal('videos', ['RelatedUrl'])

    def backwards(self, orm):
        # Deleting model 'CategoryKind'
        db.delete_table('videos_categorykind')

        # Deleting model 'Category'
        db.delete_table('videos_category')

        # Deleting model 'Speaker'
        db.delete_table('videos_speaker')

        # Deleting model 'Tag'
        db.delete_table('videos_tag')

        # Deleting model 'Video'
        db.delete_table('videos_video')

        # Removing M2M table for field tags on 'Video'
        db.delete_table('videos_video_tags')

        # Removing M2M table for field speakers on 'Video'
        db.delete_table('videos_video_speakers')

        # Deleting model 'RelatedUrl'
        db.delete_table('videos_relatedurl')

    models = {
        'videos.category': {
            'Meta': {'ordering': "['name', 'title']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.CategoryKind']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'})
        },
        'videos.categorykind': {
            'Meta': {'object_name': 'CategoryKind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
            'video_mp4_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_mp4_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_ogv_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_ogv_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_webm_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_webm_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['videos']