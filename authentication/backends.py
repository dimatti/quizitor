# coding=utf-8
from django.contrib.auth import get_user_model

class EmailAuthBackend:
    UserModel = get_user_model()

    def authenticate(self, request, username=None, email=None, password=None, force_auth=False, user_ip=None):
        try:
            user = self.UserModel.get(email=username if username else email)

            if user.check_password(password) or force_auth:
                return user
            else:
                raise Exception()
        except self.UserModel.DoesNotExist:
            return None
