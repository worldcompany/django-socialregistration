# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ('socialregistration', '0001_init'),
    )

    def forwards(self, orm):
        # Adding field 'TwitterProfile.screenname'
        db.add_column('socialregistration_twitterprofile', 'screenname', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)
        # Adding field 'TwitterProfile.consumer_key'
        db.add_column('socialregistration_twitterprofile', 'consumer_key', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)
        # Adding field 'TwitterProfile.consumer_secret'
        db.add_column('socialregistration_twitterprofile', 'consumer_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)
        # Adding field 'FacebookProfile.consumer_key'
        db.add_column('socialregistration_facebookprofile', 'consumer_key', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)
        # Adding field 'FacebookProfile.consumer_secret'
        db.add_column('socialregistration_facebookprofile', 'consumer_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

    def backwards(self, orm):
        # Deleting field 'TwitterProfile.screenname'
        db.delete_column('socialregistration_twitterprofile', 'screenname')
        # Deleting field 'TwitterProfile.consumer_key'
        db.delete_column('socialregistration_twitterprofile', 'consumer_key')
        # Deleting field 'TwitterProfile.consumer_secret'
        db.delete_column('socialregistration_twitterprofile', 'consumer_secret')
        # Deleting field 'FacebookProfile.consumer_key'
        db.delete_column('socialregistration_facebookprofile', 'consumer_key')
        # Deleting field 'FacebookProfile.consumer_secret'
        db.delete_column('socialregistration_facebookprofile', 'consumer_secret')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screenname': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['socialregistration']
