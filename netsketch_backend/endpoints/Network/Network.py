from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from netsketch_backend.authentication.auth import *
from ...models import * 

class NetworkView(APIView):  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        pk = request.GET.get("id")
        try:
            network = Network.objects.get(id=pk, user=request.user)
        except Network.DoesNotExist:
            return Response({"error": "Red no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        dispositivos = [
            {
                "id": d.pk,
                "width": d.width,
                "height": d.height,
                "image": d.image,
                "type": d.type,
                "x": d.x,
                "y": d.y,
                "configuraciones": {
                    "interfaces": [
                        {"nombre": i.name, "ip": i.ip, "mascara": i.mask, "gateway": i.gateway}
                        for i in d.interfaces.all()
                    ],
                    "tabla": [
                        {"destino": t.destiny, "destinoMascara": t.destiny_mask, "salto": t.jump}
                        for t in d.routing_tables.all()
                    ]
                }
            }
            for d in network.devices.all()
        ]
        cables = [
            {
                "from": {"id": c.from_device.pk, "interface": c.from_interface, "x": c.from_x, "y": c.from_y},
                "to": {"id": c.to_device.pk, "interface": c.to_interface, "x": c.to_x, "y": c.to_y},
                "peso": c.weight
            }
            for c in Cable.objects.filter(from_device__network=network)
        ]
        
        data = {
            "id": network.pk,
            "nombre": network.name,
            "dispositivos": dispositivos,
            "cables": cables
        }
        
        return Response({
            "success": True,
            "data": data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get("nombre")
        devices_data = request.data.get("dispositivos", [])
        cables_data = request.data.get("cables", [])
        
        if not name:
            return Response({
                "success": False,
                "data": {
                    "error": "FALTA NOMBRE"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        red = Network.objects.create(user=request.user, name=name)
        devices_map = {}

        for d in devices_data:
            device = Device.objects.create(
                network=red, 
                width=d.get("width", 0), 
                height=d.get("height", 0), 
                image=d.get("image", ""), 
                type=d.get("type", ""), 
                x=d.get("x", 0), 
                y=d.get("y", 0)
            )
            devices_map[d["id"]] = device

            configuraciones = d.get("configuraciones", [{}])  
            if isinstance(configuraciones, list) and len(configuraciones) > 0:
                configuraciones = configuraciones[0] 

            interfaces = configuraciones.get("interfaces", []) if isinstance(configuraciones, dict) else []
            for i in interfaces:
                print(i)
                Interface.objects.create(
                    device=device, 
                    name=i.get("nombre", ""), 
                    ip=i.get("ip", ""), 
                    mask=i.get("mascara", ""), 
                    gateway=i.get("gateway", "")
                )
            tabla = configuraciones.get("tabla", []) if isinstance(configuraciones, dict) else []
            for t in tabla:
                print(t)
                RoutingTable.objects.create(
                    device=device, 
                    destiny=t.get("destino", ""), 
                    destiny_mask=t.get("destinoMascara", ""), 
                    jump=t.get("salto", "")
                )

        for c in cables_data:
            Cable.objects.create(
                from_device=devices_map[c["from"]["id"]], 
                from_interface=c["from"]["interface"], 
                from_x=c["from"]["x"], 
                from_y=c["from"]["y"],
                to_device=devices_map[c["to"]["id"]], 
                to_interface=c["to"]["interface"], 
                to_x=c["to"]["x"], 
                to_y=c["to"]["y"],
                weight=c.get("peso", 0)
            )

        return Response({
            "success": True, 
            "data": {
                "message": "Red creada correctamente"
            }
        }, status=status.HTTP_201_CREATED)