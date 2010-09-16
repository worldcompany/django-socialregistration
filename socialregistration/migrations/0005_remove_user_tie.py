# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TwitterProfile.user'
        db.delete_column('socialregistration_twitterprofile', 'user_id')
        # Deleting field 'OpenIDProfile.user'
        db.delete_column('socialregistration_openidprofile', 'user_id')
        # Deleting field 'FacebookProfile.user'
        db.delete_column('socialregistration_facebookprofile', 'user_id')

    def backwards(self, orm):
        # Adding field 'TwitterProfile.user'
        db.add_column('socialregistration_twitterprofile', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)
        # Adding field 'OpenIDProfile.user'
        db.add_column('socialregistration_openidprofile', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)
        # Adding field 'FacebookProfile.user'
        db.add_column('socialregistration_facebookprofile', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'socialregistration.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'socialregistration.openidnonce': {
            'Meta': {'object_name': 'OpenIDNonce'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'socialregistration.openidprofile': {
            'Meta': {'object_name': 'OpenIDProfile'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'socialregistration.openidstore': {
            'Meta': {'object_name': 'OpenIDStore'},
            'assoc_type': ('django.db.models.fields.TextField', [], {}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.TextField', [], {}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'socialregistration.twitterprofile': {
            'Meta': {'object_name': 'TwitterProfile'},
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'screenname': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['socialregistration']
