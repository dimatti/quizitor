from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    login = models.TextField(verbose_name=_('Login'), max_length=255, unique=True)
    name = models.TextField(verbose_name=_('Name'), max_length=255, unique=True)
    surname = models.TextField(verbose_name=_('Surname'), max_length=255, unique=True)
    current_city = models.TextField(verbose_name=_('City'), max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['-id']

    def __str__(self):
        return self.email
