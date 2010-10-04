from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test import TestCase
from socialregistration.models import FacebookProfile, TwitterProfile, OpenIDProfile

class MockUser(object):
    auth = False
    def __init__(self, *args, **kwargs):
        super(MockUser, self).__init__()
        if kwargs.get('authenticated', False):
            self.auth = True

    def is_authenticated(self):
        return self.auth

class MockHttpRequest(HttpRequest):

    user = MockUser(authenticated=True)

    def __init__(self, *args, **kwargs):
        super(MockHttpRequest, self).__init__(*args, **kwargs)

        self.user.is_authenticated()

        self.session = {}

class SocialRegistrationDisconnectionTests(TestCase):

    def setUp(self):
        # set up a site object in case the current site ID doesn't exist
        site = Site.objects.get_or_create(pk=settings.SITE_ID)

    def render(self, template_string, context={}):
        """Return the rendered string or the exception raised while rendering."""
        try:
            t = template.Template(template_string)
            c = template.Context(context)
            return t.render(c)
        except Exception, e:
            return e

    def test_deregister_url_facebook(self):
        request = MockHttpRequest()
        fbp = FacebookProfile.objects.create(content_object=Site.objects.get_current(), uid=1234567890, consumer_key='aaaaaa', consumer_secret='bbbbbb')

        template = """{{ fp.get_disconnect_url }}"""
        result = self.render(template, {'request': request, 'fp': fbp,})
        self.assertEqual(result, "/socialregistration/disconnect/%s/%s/%s/" % (ContentType.objects.get_for_model(FacebookProfile).pk, ContentType.objects.get_for_model(Site).pk, fbp.object_id))

    def test_deregister_url_twitter(self):
        request = MockHttpRequest()
        twp = TwitterProfile.objects.create(content_object=Site.objects.get_current(), twitter_id=1234567890, consumer_key='aaaaaa', consumer_secret='bbbbbb')

        template = """{{ twp.get_disconnect_url }}"""
        result = self.render(template, {'request': request, 'twp': twp,})
        self.assertEqual(result, "/socialregistration/disconnect/%s/%s/%s/" % (ContentType.objects.get_for_model(TwitterProfile).pk, ContentType.objects.get_for_model(Site).pk, twp.object_id))

    def test_deregister_url_openid(self):
        request = MockHttpRequest()
        oip = OpenIDProfile.objects.create(content_object=Site.objects.get_current(), identity=1234567890)

        template = """{{ oip.get_disconnect_url }}"""
        result = self.render(template, {'request': request, 'oip': oip,})
        self.assertEqual(result, "/socialregistration/disconnect/%s/%s/%s/" % (ContentType.objects.get_for_model(OpenIDProfile).pk, ContentType.objects.get_for_model(Site).pk, oip.object_id))

    def test_deregister_facebook(self):
        # set up for it
        fbp = FacebookProfile.objects.create(content_object=Site.objects.get_current(), uid=1234567890, consumer_key='aaaaaa', consumer_secret='bbbbbb')

        settings.SOCIALREGISTRATION_DISCONNECT_URL = '/admin/' # something that should be on (nearly) every Django install to avoid 404 / other false errors

        response = self.client.post(fbp.get_disconnect_url()) # should delete it

        try:
            fbp = FacebookProfile.objects.get(content_type__id=ContentType.objects.get_for_model(Site).pk, object_id=Site.objects.get_current().pk, uid=1234567890)
            self.fail('Object should have been deleted.')
        except FacebookProfile.DoesNotExist:
            pass # delete worked

        self.assertRedirects(response, '/admin/')

    def test_deregister_twitter(self):
        # set up for it
        twp = TwitterProfile.objects.create(content_object=Site.objects.get_current(), twitter_id=1234567890, consumer_key='aaaaaa', consumer_secret='bbbbbb')

        settings.SOCIALREGISTRATION_DISCONNECT_URL = '/admin/' # something that should be on (nearly) every Django install to avoid 404 / other false errors

        response = self.client.post(twp.get_disconnect_url()) # should delete it

        try:
            twp = TwitterProfile.objects.get(content_type__id=ContentType.objects.get_for_model(Site).pk, object_id=Site.objects.get_current().pk, twitter_id=1234567890)
            self.fail('Object should have been deleted.')
        except TwitterProfile.DoesNotExist:
            pass # delete worked

        self.assertRedirects(response, '/admin/')

    def test_deregister_openid(self):
        # set up for it
        oip = OpenIDProfile.objects.create(content_object=Site.objects.get_current(), identity=1234567890)

        settings.SOCIALREGISTRATION_DISCONNECT_URL = '/admin/' # something that should be on (nearly) every Django install to avoid 404 / other false errors

        response = self.client.post(oip.get_disconnect_url()) # should delete it

        try:
            oip = OpenIDProfile.objects.get(content_type__id=ContentType.objects.get_for_model(Site).pk, object_id=Site.objects.get_current().pk, identity=1234567890)
            self.fail('Object should have been deleted.')
        except OpenIDProfile.DoesNotExist:
            pass # delete worked

        self.assertRedirects(response, '/admin/')
