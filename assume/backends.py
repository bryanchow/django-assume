from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AssumableModelBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication without a
    password.

    IMPORTANT: This backend assumes that the credentials have already been
    verified if a password is not passed to authenticate(), so all calls to
    that method should be done very carefully.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            # If no password was supplied, assume that we've already verified credentials
            if password == None:
                return user
            # Otherwise, check the password
            elif user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class AssumableEmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows logging in using either username
    or email address, and allows authentication without a password.

    IMPORTANT: This backend assumes that the credentials have already been
    verified if a password is not passed to authenticate(), so all calls to
    that method should be done very carefully.
    """

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            # If no password was supplied, assume that we've already verified credentials
            if password == None:
                return user
            # Otherwise, check the password
            elif user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
