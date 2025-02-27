from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from netsketch_backend.models import Network
from django.utils.timezone import utc

class UserNetworksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            networks = Network.objects.filter(user=request.user).values("id", "name", "creation_date")
            
            data = {
                "success": True,
                "data": [
                    {
                        "id": net["id"],
                        "nombre": net["name"],
                        "fecha_creacion": net["creation_date"].astimezone(utc).isoformat() if net["creation_date"] else ""
                    }
                    for net in networks
                ]
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "data": {"error": str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
