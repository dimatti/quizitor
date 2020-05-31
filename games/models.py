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


    def create_new(cls, name, points, questions, answers, tips):
        """
        name: string
        points: list of tuples(lat, lon)
        questions: list of str
        answers: list of str
        tips: list of str
        """
        if len(points) != len(questions) != len(answers) != len(tips):
            raise Exception("create error")
        points_lat, points_lon = []
        for pair in points:
            points_lat.append(pair[0])
            points_lat.append(1)