from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import User

# Create your views here.

class UserView(APIView):
    def get(self, request, pk):
        print(pk)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({"success": "User '{}' created successfully".format(user_saved.username)})

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(User.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "User with id `{}` has been deleted.".format(pk)
        }, status=204)
