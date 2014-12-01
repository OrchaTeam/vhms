from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model, Q
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator
from apps.profiles.models import Profile

class VHMSProfileModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        if username:
            username_or_email = Q(username=username) | Q(email=username)
            try:
                profile = Profile.objects.get(username_or_email, **kwargs)
                if profile.check_password(password):
                    return profile
            except Profile.DoesNotExist:
                pass
        else:
            if 'uidb36' not in kwargs:
                return
            kwargs["id"] = base36_to_int(kwargs.pop("uidb36"))
            token = kwargs.pop("token")
            try:
                profile = Profile.objects.get(**kwargs)
            except Profile.DoesNotExist:
                print("hello")
            else:
                if default_token_generator.check_token(profile, token):
                    return profile

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None


