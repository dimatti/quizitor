from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

import pyproj

DISTANCE = 50.0


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
        return user_answer.lower() == self.answer.lower()

    @classmethod
    def new_point(cls, lat, lon, is_node=False, question="", answer="", tip=""):
        p = Point(lat=lat, lon=lon, is_node=is_node, question=question, answer=answer, tip=tip)
        p.save()
        return p


class Cluster(models.Model):
    start = models.ForeignKey(Point, related_name='cluster_point_start', on_delete=models.CASCADE)
    finish = models.ForeignKey(Point, related_name='cluster_point_finish', on_delete=models.CASCADE)
    points = models.ManyToManyField(Point)

    objects = models.Manager()

    @classmethod
    def new_cluster(cls, data):
        start = Point.new_point(data["start"][0], data["start"][1], is_node=True)
        finish = Point.new_point(data["finish"][0], data["finish"][1], is_node=True)
        c = Cluster(start=start, finish=finish)
        c.save()
        points_data = data["points"]
        for p in points_data:
            c.points.add(Point.new_point(p["lat"], p["lon"], is_node=False, question=p["question"], answer=p["answer"],
                                         tip=p["tip"]))
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
    is_checked = models.BooleanField(verbose_name=_('Is Checked'), default=False)
    objects = models.Manager()

    @classmethod
    def new_result_point(cls, point):
        rp = ResultPoint(point=point)
        rp.save()
        return rp

    def check_point(self, lat, lon):
        res = self.point.check_point(lat, lon)
        if res:
            self.is_checked = res
            self.save()
        return res

    def check_answer(self, answer):
        self.user_answer = answer
        self.is_answered_correctly = self.point.check_answer(answer)
        self.time_completed = datetime.now()
        self.save()
        return self.is_answered_correctly

    def get_tip(self):
        tip = self.point.tip
        self.is_tip_used = True
        self.save()
        return tip

    def get_distance(self, lat, lon):
        return self.point.get_distance(lat, lon)

    def get_help(self):
        self.is_help_used = True
        self.save()
        return self.point.lat, self.point.lon

    def get_status(self):
        status = {"is_answered_correctly": self.is_answered_correctly,
                  "is_help_used": self.is_help_used,
                  "is_tip_used": self.is_tip_used,
                  "time_completed": self.time_completed,
                  "is_checked": self.is_checked,
                  "coordinates": {}}
        if self.is_checked:
            status["coordinates"] = {"lat": self.point.lat, "lon": self.point.lon}
        return status


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
        results = {}
        i = 0
        for point in self.results.all():
            results[i] = point.get_distance(lat, lon)
            i += 1
        return results

    def check_point(self, index, lat, lon):
        points = self.results.all()
        result = points[index].check_point(lat, lon)
        return result

    def check_points(self, lat, lon):
        points = self.results.all()
        for i in range(len(points)):
            if points[i].check_point(lat, lon):
                return True, i, points[i].point.lat, points[i].point.lon
        return False, -1, 0, 0

    def get_help(self, index):
        points = self.results.all()
        result = points[index].get_help()
        return result

    def check_answer(self, index, answer):
        points = self.results.all()
        result = points[index].check_answer(answer)
        return result

    def get_question(self, index):
        points = self.results.all()
        result = points[index].point.question
        return result

    def get_tip(self, index):
        points = self.results.all()
        result = points[index].get_tip()
        return result

    def get_status(self):
        results = {"id": self.pk, "start": {"lat": self.cluster.start.lat, "lon": self.cluster.start.lon},
                   "finish": {"lat": self.cluster.finish.lat, "lon": self.cluster.finish.lon}}
        i = 0
        points = []
        for point in self.results.all():
            points.append(point.get_status())
            i += 1
            results["points"] = points
        return results

    def close_cluster(self, forced=False):
        status = self.get_status()
        scores = 0
        for index in status:
            s = status[index]
            if not s["is_checked"]:
                if forced:
                    return 0
                return None
            scores += get_point_score(s)
        scores += get_time_score(self.time_start)
        self.time_completed = datetime.now()
        self.scores = scores
        self.save()
        return scores


def get_time_score(time_start):
    result = 100 - (datetime.now().replace(tzinfo=None) - time_start.replace(tzinfo=None)).seconds
    if result < 0:
        return 0
    return result


def get_point_score(status):
    score = 0
    if not status["is_answered_correctly"]:
        return 0
    score += 5
    if not status["is_tip_used"]:
        score += 5
    if not status["is_help_used"]:
        score += 5
    return score


class CurrentGame(models.Model):
    source_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    results = models.ManyToManyField(ResultCluster)
    time_start = models.DateTimeField(verbose_name=_('Time Start'))
    time_completed = models.DateTimeField(verbose_name=_('Time Completed'), null=True)
    scores = models.IntegerField(verbose_name=_('Scores'), default=0)

    objects = models.Manager()

    def next_cluster(self):
        original_clusters = self.source_game.clusters.all()
        results = self.results.all()
        if len(results) < len(original_clusters):
            result = ResultCluster.new_result_cluster(original_clusters[len(results)])
            self.results.add(result)
            return result
        return None

    def current_cluster(self):
        if len(self.results.all()) > 0:
            return self.results.all()[len(self.results.all()) - 1]
        return None

    def close_current_game(self):
        scores = 0
        for cluster in self.results.all():
            scores += cluster.scores
        self.time_completed = datetime.now()
