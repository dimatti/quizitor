from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser):
    username = models.TextField(verbose_name=_('Username'), max_length=255, unique=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    name = models.TextField(verbose_name=_('Name'), max_length=255, unique=True)
    surname = models.TextField(verbose_name=_('Surname'), max_length=255, unique=True)
    current_city = models.TextField(verbose_name=_('City'), max_length=255, unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    is_staff = models.BooleanField(verbose_name=_('Is staff'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Is superuser'), default=False)

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['-id']

    def __str__(self):
        return self.email

