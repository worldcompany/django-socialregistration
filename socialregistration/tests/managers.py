from django import template
from django.conf import settings
from django.contrib.auth.models import User
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

class SocialRegistrationManagerTests(TestCase):

    def setUp(self):
        # set up a site object in case the current site ID doesn't exist
        site = Site.objects.get_or_create(pk=settings.SITE_ID)
        # and users
        self.user1 = User.objects.get_or_create(username='user1')[0]
        self.user2 = User.objects.get_or_create(username='user2')[0]

    def render(self, template_string, context={}):
        """Return the rendered string or the exception raised while rendering."""
        try:
            t = template.Template(template_string)
            c = template.Context(context)
            return t.render(c)
        except Exception, e:
            return e

    def test_twitter_for_user_by_username(self):
        try:
            tp = TwitterProfile.objects.for_user_by_username(self.user1.username)
            self.fail('Twitter profile existed and should not have.')
        except TwitterProfile.DoesNotExist:
            pass

        tp1 = TwitterProfile.objects.create(content_object=self.user1, twitter_id=1)

        try:
            tp = TwitterProfile.objects.for_user_by_username(self.user1.username)
        except TwitterProfile.DoesNotExist:
            self.fail('Twitter profile did not exist and should have.')

        tp1.delete()

    def test_twitter_for_user_by_id(self):
        try:
            tp = TwitterProfile.objects.for_user_by_id(self.user1.pk)
            self.fail('Twitter profile existed and should not have.')
        except TwitterProfile.DoesNotExist:
            pass

        tp1 = TwitterProfile.objects.create(content_object=self.user1, twitter_id=1)

        try:
            tp = TwitterProfile.objects.for_user_by_id(self.user1.pk)
        except TwitterProfile.DoesNotExist:
            self.fail('Twitter profile did not exist and should have.')

        tp1.delete()

    def test_twitter_for_object(self):
        try:
            tp = TwitterProfile.objects.for_object(self.user1)
            self.fail('Twitter profile existed and should not have.')
        except TwitterProfile.DoesNotExist:
            pass

        tp1 = TwitterProfile.objects.create(content_object=self.user1, twitter_id=1)

        try:
            tp = TwitterProfile.objects.for_object(self.user1)
        except TwitterProfile.DoesNotExist:
            self.fail('Twitter profile did not exist and should have.')

        tp1.delete()

    def test_twitter_for_object_content_type(self):
        self.assertEqual(TwitterProfile.objects.for_object_content_type(self.user1).count(), 0)
        tp1 = TwitterProfile.objects.create(content_object=self.user1, twitter_id=1)
        self.assertEqual(TwitterProfile.objects.for_object_content_type(self.user1).count(), 1)
        tp1.delete()

    def test_facebook_for_user_by_username(self):
        try:
            fp = FacebookProfile.objects.for_user_by_username(self.user1.username)
            self.fail('Facebook profile existed and should not have.')
        except FacebookProfile.DoesNotExist:
            pass

        fp1 = FacebookProfile.objects.create(content_object=self.user1)

        try:
            fp = FacebookProfile.objects.for_user_by_username(self.user1.username)
        except FacebookProfile.DoesNotExist:
            self.fail('Facebook profile did not exist and should have.')

        fp1.delete()

    def test_facebook_for_user_by_id(self):
        try:
            fp = FacebookProfile.objects.for_user_by_id(self.user1.pk)
            self.fail('Facebook profile existed and should not have.')
        except FacebookProfile.DoesNotExist:
            pass

        fp1 = FacebookProfile.objects.create(content_object=self.user1)

        try:
            tp = FacebookProfile.objects.for_user_by_id(self.user1.pk)
        except FacebookProfile.DoesNotExist:
            self.fail('Facebook profile did not exist and should have.')

        fp1.delete()

    def test_facebook_for_object(self):
        try:
            fp = FacebookProfile.objects.for_object(self.user1)
            self.fail('Facebook profile existed and should not have.')
        except FacebookProfile.DoesNotExist:
            pass

        fp1 = FacebookProfile.objects.create(content_object=self.user1)

        try:
            fp = FacebookProfile.objects.for_object(self.user1)
        except FacebookProfile.DoesNotExist:
            self.fail('Facebook profile did not exist and should have.')

        fp1.delete()

    def test_facebook_for_object_content_type(self):
        self.assertEqual(FacebookProfile.objects.for_object_content_type(self.user1).count(), 0)
        fp1 = FacebookProfile.objects.create(content_object=self.user1)
        self.assertEqual(FacebookProfile.objects.for_object_content_type(self.user1).count(), 1)
        fp1.delete()

    def test_openid_for_user_by_username(self):
        try:
            op = OpenIDProfile.objects.for_user_by_username(self.user1.username)
            self.fail('OpenID profile existed and should not have.')
        except OpenIDProfile.DoesNotExist:
            pass

        op1 = OpenIDProfile.objects.create(content_object=self.user1)

        try:
            op = OpenIDProfile.objects.for_user_by_username(self.user1.username)
        except OpenIDProfile.DoesNotExist:
            self.fail('OpenID profile did not exist and should have.')

        op1.delete()

    def test_openid_for_user_by_id(self):
        try:
            op = OpenIDProfile.objects.for_user_by_id(self.user1.pk)
            self.fail('OpenID profile existed and should not have.')
        except OpenIDProfile.DoesNotExist:
            pass

        op1 = OpenIDProfile.objects.create(content_object=self.user1)

        try:
            op = OpenIDProfile.objects.for_user_by_id(self.user1.pk)
        except OpenIDProfile.DoesNotExist:
            self.fail('OpenID profile did not exist and should have.')

        op1.delete()

    def test_openid_for_object(self):
        try:
            op = OpenIDProfile.objects.for_object(self.user1)
            self.fail('OpenID profile existed and should not have.')
        except OpenIDProfile.DoesNotExist:
            pass

        op1 = OpenIDProfile.objects.create(content_object=self.user1)

        try:
            op = OpenIDProfile.objects.for_object(self.user1)
        except OpenIDProfile.DoesNotExist:
            self.fail('OpenID profile did not exist and should have.')

        op1.delete()

    def test_openid_for_object_content_type(self):
        self.assertEqual(OpenIDProfile.objects.for_object_content_type(self.user1).count(), 0)
        op1 = OpenIDProfile.objects.create(content_object=self.user1)
        self.assertEqual(OpenIDProfile.objects.for_object_content_type(self.user1).count(), 1)
        op1.delete()
