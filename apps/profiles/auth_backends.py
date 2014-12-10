from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.models import User

class VHMSProfileModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        if username:
            username_or_email = Q(username=username) | Q(email=username)
            try:
                user = User.objects.get(username_or_email, **kwargs)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
        else:
            if 'uidb36' not in kwargs:
                return
            kwargs["id"] = base36_to_int(kwargs.pop("uidb36"))
            token = kwargs.pop("token")
            try:
                user = User.objects.get(**kwargs)
            except User.DoesNotExist:
                pass
            else:
                if default_token_generator.check_token(user, token):
                    return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


