from datetime import datetime

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

from .models import Game, CurrentGame, Cluster, ResultCluster


class CurrentGameInitView(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        game = Game.objects.get(id=pk)
        cg = CurrentGame(source_game=game, time_start=datetime.now())
        cg.save()
        return Response({"id": cg.id})


class MiniGameViewSet(viewsets.ViewSet):
    queryset = Cluster.objects.all()

    @action(detail=False, methods=["POST"])
    def set_data(self, request):
        data = request.data
        cluster = Cluster.new_cluster(data=data)
        return Response({"id": cluster.pk})

    @action(detail=False, methods=["POST"])
    def start_game(self, request):
        data = request.data
        id = data["id"]
        cluster = ResultCluster.new_result_cluster(Cluster.objects.get(pk=id))
        return Response(cluster.get_status())

    @action(detail=False, methods=["POST"])
    def get_status(self, request):
        data = request.data
        id = data["id"]
        cluster = ResultCluster.objects.get(pk=id)
        return Response(cluster.get_status())

    @action(detail=False, methods=["POST"])
    def get_distances(self, request):
        data = request.data
        id = data["id"]
        lat = data["lat"]
        lon = data["lon"]
        cluster = ResultCluster.objects.get(pk=id)
        return Response(cluster.get_points_info(lat, lon))

    @action(detail=False, methods=["POST"])
    def check(self, request):
        data = request.data
        id = data["id"]
        lat = data["lat"]
        lon = data["lon"]
        cluster = ResultCluster.objects.get(pk=id)
        result, index, lat, lon = cluster.check_points(lat, lon)
        return Response({"point": index, "result": result, "lat": lat, "lon": lon})

    @action(detail=False, methods=["POST"])
    def get_question(self, request):
        data = request.data
        id = data["id"]
        num = data["num"]
        cluster = ResultCluster.objects.get(pk=id)
        question = cluster.get_question(num)
        return Response({"question": question})

    @action(detail=False, methods=["POST"])
    def get_tip(self, request):
        data = request.data
        id = data["id"]
        num = data["num"]
        cluster = ResultCluster.objects.get(pk=id)
        tip = cluster.get_tip(num)
        return Response({"tip": tip})

    @action(detail=False, methods=["POST"])
    def check_answer(self, request):
        data = request.data
        id = data["id"]
        num = data["num"]
        answer = data["answer"]
        cluster = ResultCluster.objects.get(pk=id)
        question = cluster.check_answer(num, answer)
        return Response({"question": question})
