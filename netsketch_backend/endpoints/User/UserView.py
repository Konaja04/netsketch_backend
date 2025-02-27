from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from netsketch_backend.authentication.auth import *



#USER DATA   
class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            data = {
                "success": True,
                "data": {'username': user.username, 'email': user.email, "identifier": user.identifier}
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "success": False,
                "data": {"error":e}
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   