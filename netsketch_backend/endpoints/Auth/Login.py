from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from netsketch_backend.authentication.auth import *

#AUTH
class LoginView(APIView):  
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            user.is_superuser = True
            token, created = Token.objects.get_or_create(user=user)
            if created:
                print("Token created for user:", user.email)
            else:
                print("Token retrieved for user:", user.email)
            data = {
                "success": True,
                "data":  {
                    'token': token.key
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False, 
                'data': {'error': 'Invalid Credentials'}
            }, status=status.HTTP_401_UNAUTHORIZED)
