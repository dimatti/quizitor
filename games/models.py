from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Game(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    points_lat = models.FloatField(verbose_name=_('Point Latitude'))
    points_lon = models.FloatField(verbose_name=_('Point Longitude'))
    questions = models.TextField(verbose_name=_('Question'))
    answers = models.TextField(verbose_name=_('Answer'))
    tips = models.TextField(verbose_name=_('Tip'))

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ['-id']
