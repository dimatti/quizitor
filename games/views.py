from datetime import datetime

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

from .models import Game, CurrentGame


class CurrentGameInitView(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        game = Game.objects.get(id=pk)
        cg = CurrentGame(source_game=game, time_start=datetime.now())
        cg.save()
        return Response({"id": cg.id})

