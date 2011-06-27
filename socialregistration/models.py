from django.db import models

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site 

from socialregistration.managers import SocialProfileManager

class FacebookProfile(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    site = models.ForeignKey(Site, default=Site.objects.get_current)
    uid = models.CharField(max_length=255, blank=False, null=False)
    consumer_key = models.CharField('AKA access_token', max_length=128)
    consumer_secret = models.CharField('AKA secret', max_length=128)

    objects = SocialProfileManager()

    def __unicode__(self):
        return u'%s: %s' % (self.content_object, self.uid)

    def authenticate(self):
        return authenticate(uid=self.uid)

    def get_disconnect_url(self):
        return reverse('disconnect', kwargs={'network': ContentType.objects.get_for_model(self.__class__).pk, 'object_type': self.content_type.pk, 'object_id': self.object_id})

class TwitterProfile(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    site = models.ForeignKey(Site, default=Site.objects.get_current)
    twitter_id = models.PositiveIntegerField()
    screenname = models.CharField(max_length=40, null=True)
    consumer_key = models.CharField(max_length=128)
    consumer_secret = models.CharField(max_length=128)

    objects = SocialProfileManager()

    def __unicode__(self):
        return u'%s: %s' % (self.content_object, self.twitter_id)

    def authenticate(self):
        return authenticate(twitter_id=self.twitter_id)

    def get_disconnect_url(self):
        return reverse('disconnect', kwargs={'network': ContentType.objects.get_for_model(self.__class__).pk, 'object_type': self.content_type.pk, 'object_id': self.object_id})

class OpenIDProfile(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    site = models.ForeignKey(Site, default=Site.objects.get_current)
    identity = models.TextField()

    objects = SocialProfileManager()

    def __unicode__(self):
        return u'OpenID Profile for %s, via provider %s' % (self.content_object, self.identity)

    def authenticate(self):
        return authenticate(identity=self.identity)

    def get_disconnect_url(self):
        return reverse('disconnect', kwargs={'network': ContentType.objects.get_for_model(self.__class__).pk, 'object_type': self.content_type.pk, 'object_id': self.object_id})

class OpenIDStore(models.Model):
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.TextField()
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField()

    def __unicode__(self):
        return u'OpenID Store %s for %s' % (self.server_url, self.site)

class OpenIDNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'OpenID Nonce for %s' % self.server_url
