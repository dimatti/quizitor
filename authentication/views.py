from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status

class UserAuthorization(APIView):

    def post(self, request):
        username = request.POST.get('login', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({"status": "Ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Some error with authorization"},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        if user is not None:
            return Response({"id": user.id})
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)
