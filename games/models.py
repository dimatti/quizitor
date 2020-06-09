from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

import pyproj

DISTANCE = 10.0


class Point(models.Model):
    lat = models.FloatField(verbose_name=_('Point Latitude'))
    lon = models.FloatField(verbose_name=_('Point Longitude'))
    is_node = models.BooleanField(verbose_name=_('Is Node'), default=False)
    question = models.TextField(verbose_name=_('Question'), null=True)
    answer = models.TextField(verbose_name=_('Answer'), null=True)
    tip = models.TextField(verbose_name=_('Tip'), null=True)

    objects = models.Manager()

    def get_distance(self, lat_user, lon_user):
        geodesic = pyproj.Geod(ellps='WGS84')
        return geodesic.inv(lat_user, lon_user, self.lat, self.lon)

    def check_point(self, lat_user, lon_user):
        _, _, distance = self.get_distance(lat_user, lon_user)
        return abs(distance) < DISTANCE

    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer

    @classmethod
    def new_point(cls, lat, lon, is_node=False, question="", answer="", tip=""):
        p = Point(lat=lat, lon=lon, is_node=is_node, question=question, answer=answer, tip=tip)
        p.save()
        return p


class Cluster(models.Model):
    start = models.ForeignKey(Point,  related_name='cluster_point_start', on_delete=models.CASCADE)
    finish = models.ForeignKey(Point,  related_name='cluster_point_finish',  on_delete=models.CASCADE)
    points = models.ManyToManyField(Point)

    objects = models.Manager()

    @classmethod
    def new_cluster(cls, data):
        start = Point.new_point(data["start"][0], data["start"][1], is_node=True)
        finish = Point.new_point(data["start"][0], data["start"][1], is_node=True)
        c = Cluster(start=start, finish=finish)
        c.save()
        points_data = data["points"]
        for p in points_data:
            c.points.add(Point.new_point(p["lat"], p["lon"], is_node=False, question=p["question"], answer=p["answer"], tip=p["tip"]))
        c.save()
        return c


class Game(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    clusters = models.ManyToManyField(Cluster)

    objects = models.Manager()

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ['-id']

    @classmethod
    def new_game(cls, data):
        g = Game(name=data["name"])
        g.save()
        for cluster in data["clusters"]:
            g.clusters.add(Cluster.new_cluster(cluster))
        g.save()
        return g


class ResultPoint(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    time_completed = models.DateTimeField(verbose_name=_('Time Completed'), null=True)
    user_answer = models.TextField(verbose_name=_('User Answer'), null=True)
    is_answered_correctly = models.BooleanField(verbose_name=_('Is Answered Correctly'), default=False)
    is_tip_used = models.BooleanField(verbose_name=_('Is Tip Used'), default=False)
    is_help_used = models.BooleanField(verbose_name=_('Is Help Used'), default=False)
    is_checked_correctly = models.BooleanField(verbose_name=_('Is Checked Correctly'), default=False)

    objects = models.Manager()

    @classmethod
    def new_result_point(cls, point):
        rp = ResultPoint(point=point)
        rp.save()
        return rp

    def check_point(self, lat, lon):
        res = self.point.check_point(lat, lon)
        self.is_checked_correctly = res
        self.save()
        return res

    def check_answer(self, answer):
        self.user_answer = answer
        self.is_answered_correctly = self.point.check_answer(answer)
        return self.is_answered_correctly

    def get_tip(self):
        tip = self.point.tip
        self.is_tip_used = True
        self.save()
        return tip

    def get_distance(self, lat, lon):
        return self.point.get_distance(lat, lon)

    def get_real_point_info(self):
        return self.point.lat, self.point.lon


class ResultCluster(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    time_start = models.DateTimeField(verbose_name=_('Time Start'))
    time_completed = models.DateTimeField(verbose_name=_('Time Completed'), null=True)
    scores = models.IntegerField(verbose_name=_('Scores'))
    results = models.ManyToManyField(ResultPoint)
    objects = models.Manager()

    @classmethod
    def new_result_cluster(cls, cluster):
        rc = ResultCluster(cluster=cluster, time_start=datetime.now(), scores=0)
        rc.save()
        for p in cluster.points.all():
            rp = ResultPoint.new_result_point(p)
            rc.results.add(rp)
        rc.save()
        return rc

    def get_points_info(self, lat, lon):
        results = []
        for point in self.results:
            results.append(point.get_distance(lat, lon))
        return results

    # def get_cluster_info(self):
    #     response = {}
    #     for


class CurrentGame(models.Model):
    source_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    results = models.ManyToManyField(ResultCluster)
    time_start = models.DateTimeField(verbose_name=_('Time Start'))
    time_completed = models.DateTimeField(verbose_name=_('Time Completed'), null=True)
    scores = models.IntegerField(verbose_name=_('Scores'), default=0)

    objects = models.Manager()

    def next_cluster(self):
        original_clusters = self.source_game.clasters.all()
        results = self.results.all()
        if len(results) < len(original_clusters):
            result = ResultCluster.new_result_cluster(original_clusters[len(results)])
            self.source_game.clasters.add(result)
            return result
        return None

    def current_cluster(self):
        return self.results.all()[-1]

