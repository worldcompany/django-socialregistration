from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models

class FacebookProfileManager(models.Manager):
    def for_user_by_username(self, username):
        user = User.objects.get(username=username)
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user.id)

    def for_user_by_id(self, user_id):
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user_id)

class TwitterProfileManager(models.Manager):
    def for_user_by_username(self, username):
        user = User.objects.get(username=username)
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user.id)

    def for_user_by_id(self, user_id):
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user_id)

class OpenIDProfileManager(models.Manager):
    def for_user_by_username(self, username):
        user = User.objects.get(username=username)
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user.id)

    def for_user_by_id(self, user_id):
        return self.get(content_type=ContentType.objects.get_for_model(User), object_id=user_id)
