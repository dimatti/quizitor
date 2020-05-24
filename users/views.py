from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import User

# Create your views here.

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({"success": "User '{}' created successfully".format(user_saved.username)})

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(User.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "User with id `{}` has been deleted.".format(pk)
        }, status=204)

    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = UserSerializer(instance=saved_user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_user = serializer.save()
        return Response({
            "success": "User '{}' updated successfully".format(saved_user.username)
        })
