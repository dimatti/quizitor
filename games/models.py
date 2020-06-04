from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Point(models.Model):
    lat = models.FloatField(verbose_name=_('Point Latitude'))
    lon = models.FloatField(verbose_name=_('Point Longitude'))
    is_node = models.BooleanField(verbose_name=_('Is Node'), default=False)
    question = models.TextField(verbose_name=_('Question'), null=True)
    answer = models.TextField(verbose_name=_('Answer'), null=True)
    tip = models.TextField(verbose_name=_('Tip'), null=True)


class Game(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    points = models.ManyToManyField(Point)

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ['-id']


class Result(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    time_completed = models.DateTimeField(verbose_name=_('Time Completed'))
    user_answer = models.TextField(verbose_name=_('User Answer'), null=True)
    is_answered_correctly = models.BooleanField(verbose_name=_('Is Answered Correctly'), default=False)
    is_checked_correctly = models.BooleanField(verbose_name=_('Is Checked Correctly'), default=False)


class CurrentGame(models.Model):
    source_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    results = models.ManyToManyField(Result)
    time_start = models.DateTimeField(verbose_name=_('Time Start'))
