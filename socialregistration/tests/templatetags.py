from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test import TestCase

class MockUser(object):
    auth = False
    def __init__(self, *args, **kwargs):
        super(MockUser, self).__init__(*args, **kwargs)
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

class SocialRegistrationTemplateTagTests(TestCase):

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

    def test_open_id_error(self):
        request = MockHttpRequest()

        request.session['openid_error'] = True
        request.session['openid_provider'] = 'whizzle'

        template = """{% load socialregistration_tags %}{% open_id_errors request %}{{ openid_error }}|{{ openid_provider }}"""
        result = self.render(template, {'request': request,})
        self.assertEqual(result, u'True|whizzle')

        # but accessing it a second time, the error should have cleared.
        template = """{% load socialregistration_tags %}{% open_id_errors request %}{{ openid_error }}|{{ openid_provider }}"""
        result = self.render(template, {'request': request,})
        self.assertEqual(result, u'False|')

    def test_auth_enabled(self):
        # store what it used to be
        pre_conf = {
            'FACEBOOK_API_KEY': getattr(settings, 'FACEBOOK_API_KEY', ''),
            'FACEBOOK_SECRET_KEY': getattr(settings, 'FACEBOOK_SECRET_KEY', ''),
            'TWITTER_CONSUMER_KEY': getattr(settings, 'TWITTER_CONSUMER_KEY', ''),
            'TWITTER_CONSUMER_SECRET_KEY': getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', ''),
            'TWITTER_REQUEST_TOKEN_URL': getattr(settings, 'TWITTER_REQUEST_TOKEN_URL', ''),
            'TWITTER_ACCESS_TOKEN_URL': getattr(settings, 'TWITTER_ACCESS_TOKEN_URL', ''),
            'TWITTER_AUTHORIZATION_URL': getattr(settings, 'TWITTER_AUTHORIZATION_URL', ''),
        }

        # now remove and test, all should return nothing (not enabled)
        settings.FACEBOOK_API_KEY = ''
        settings.FACEBOOK_SECRET_KEY = ''
        settings.TWITTER_CONSUMER_KEY = ''
        settings.TWITTER_CONSUMER_SECRET_KEY = ''
        settings.TWITTER_REQUEST_TOKEN_URL = ''
        settings.TWITTER_ACCESS_TOKEN_URL = ''
        settings.TWITTER_AUTHORIZATION_URL = ''

        template = """{% load socialregistration_tags %}{% auth_enabled facebook as facebook_enabled %}{% if facebook_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')

        template = """{% load socialregistration_tags %}{% auth_enabled twitter as twitter_enabled %}{% if twitter_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')

        template = """{% load socialregistration_tags %}{% auth_enabled faCeBoOk as facebook_enabled %}{% if facebook_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')

        template = """{% load socialregistration_tags %}{% auth_enabled TwiTtER as twitter_enabled %}{% if twitter_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')

        # now re-add and test, all should return affirmative
        settings.FACEBOOK_API_KEY = 'aabc'
        settings.FACEBOOK_SECRET_KEY = 'bbvr'
        settings.TWITTER_CONSUMER_KEY = 'bnvr'
        settings.TWITTER_CONSUMER_SECRET_KEY = 'yrhf'
        settings.TWITTER_REQUEST_TOKEN_URL = 'qinv'
        settings.TWITTER_ACCESS_TOKEN_URL = 'pecg'
        settings.TWITTER_AUTHORIZATION_URL = 'mnoy'

        template = """{% load socialregistration_tags %}{% auth_enabled facebook as facebook_enabled %}{% if facebook_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'yep')

        template = """{% load socialregistration_tags %}{% auth_enabled twitter as twitter_enabled %}{% if twitter_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'yep')

        template = """{% load socialregistration_tags %}{% auth_enabled faCeBoOk as facebook_enabled %}{% if facebook_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'yep')

        template = """{% load socialregistration_tags %}{% auth_enabled TwiTtER as twitter_enabled %}{% if twitter_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'yep')

        # make sure everything has to be fully set up to work
        settings.TWITTER_AUTHORIZATION_URL = ''
        settings.FACEBOOK_SECRET_KEY = ''

        template = """{% load socialregistration_tags %}{% auth_enabled twitter as twitter_enabled %}{% if twitter_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')

        template = """{% load socialregistration_tags %}{% auth_enabled facebook as facebook_enabled %}{% if facebook_enabled %}yep{% endif %}"""
        result = self.render(template, {})
        self.assertEqual(result, u'')


        # now restore
        settings.FACEBOOK_API_KEY = pre_conf['FACEBOOK_API_KEY']
        settings.FACEBOOK_SECRET_KEY = pre_conf['FACEBOOK_SECRET_KEY']
        settings.TWITTER_CONSUMER_KEY = pre_conf['TWITTER_CONSUMER_KEY']
        settings.TWITTER_CONSUMER_SECRET_KEY = pre_conf['TWITTER_CONSUMER_SECRET_KEY']
        settings.TWITTER_REQUEST_TOKEN_URL = pre_conf['TWITTER_REQUEST_TOKEN_URL']
        settings.TWITTER_ACCESS_TOKEN_URL = pre_conf['TWITTER_ACCESS_TOKEN_URL']
        settings.TWITTER_AUTHORIZATION_URL = pre_conf['TWITTER_AUTHORIZATION_URL']

    def test_object_to_twitter_button(self):
        request = MockHttpRequest()

        template = """{% load twitter_tags %}{% twitter_button %}"""
        # "normal" / backwards-compatible - sets nothing, leading to the social credentials being attached to the current user
        result = self.render(template, {'request': request})
        self.assertEqual(result, """\n<form class="connect-button" name="login" method="post" action="/socialregistration/twitter/redirect/">\n\n\n<input type="image" onclick="this.form.submit();" src="http://apiwiki.twitter.com/f/1242697608/Sign-in-with-Twitter-lighter.png" />\n</form>\n""")

        # leads to the item in content_object being stashed and the social credentials being attached to it instead of the current user
        result = self.render(template, {'request': request, 'socialregistration_connect_object': Site.objects.get_current(),})
        self.assertEqual(result, """\n<form class="connect-button" name="login" method="post" action="/socialregistration/twitter/redirect/?a=sites&m=site&i=1">\n\n\n<input type="image" onclick="this.form.submit();" src="http://apiwiki.twitter.com/f/1242697608/Sign-in-with-Twitter-lighter.png" />\n</form>\n""")

    def test_object_to_facebook_button(self):
        request = MockHttpRequest()

        template = """{% load facebook_tags %}{% facebook_button %}"""
        # "normal" / backwards-compatible - sets nothing, leading to the social credentials being attached to the current user
        result = self.render(template, {'request': request})
        self.assertEqual(result, """\n\n\n<form class="connect-button" name="login" method="post" action="/socialregistration/facebook/connect/">\n\n\n<input type="image" onclick="facebookConnect(this.form);return false;" src="http://static.ak.fbcdn.net/images/fbconnect/login-buttons/connect_light_large_long.gif" />\n</form>\n""")

        # leads to the item in content_object being stashed and the social credentials being attached to it instead of the current user
        result = self.render(template, {'request': request, 'socialregistration_connect_object': Site.objects.get_current(),})
        self.assertEqual(result, """\n\n\n<form class="connect-button" name="login" method="post" action="/socialregistration/facebook/connect/?a=sites&m=site&i=1">\n\n\n<input type="image" onclick="facebookConnect(this.form);return false;" src="http://static.ak.fbcdn.net/images/fbconnect/login-buttons/connect_light_large_long.gif" />\n</form>\n""")

    def test_object_to_openid_button(self):
        request = MockHttpRequest()

        template = """{% load openid_tags %}{% openid_form %}"""
        # "normal" / backwards-compatible - sets nothing, leading to the social credentials being attached to the current user
        result = self.render(template, {'request': request})
        self.assertEqual(result, """<form action="/socialregistration/openid/redirect/" method="GET">\n    <input type="text" name="openid_provider" />\n\n    <input type="submit" value="Connect with OpenID" />\n</form>\n""")

        # leads to the item in content_object being stashed and the social credentials being attached to it instead of the current user
        result = self.render(template, {'request': request, 'socialregistration_connect_object': Site.objects.get_current(),})
        self.assertEqual(result, """<form action="/socialregistration/openid/redirect/" method="GET">\n    <input type="text" name="openid_provider" />\n\n    <input type="hidden" name="a" value="sites">\n    <input type="hidden" name="m" value="site">\n    <input type="hidden" name="i" value="1">\n\n    <input type="submit" value="Connect with OpenID" />\n</form>\n""")
