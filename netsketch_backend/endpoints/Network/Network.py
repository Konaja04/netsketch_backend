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
            return Response({
                "success": False,
                "data": {
                    "error": "RED NO ENCONTRADA"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        dispositivos = [
            {
                "id": d.pk,
                "width": d.width or "",  
                "height": d.height or "",  
                "image": d.image or "",  
                "type": d.type or "",  
                "x": d.x or "",  
                "y": d.y or "",  
                "configuraciones": {
                    "interfaces": [
                        {
                            "nombre": i.name or "", 
                            "ip": i.ip or "", 
                            "mascara": i.mask or "", 
                            "gateway": i.gateway or ""
                        }
                        for i in d.interfaces.all()
                    ],
                    "tabla": [
                        {
                            "destino": t.destiny or "", 
                            "destinoMascara": t.destiny_mask or "", 
                            "salto": t.jump or ""
                        }
                        for t in d.routing_tables.all()
                    ]
                }
            }
            for d in network.devices.all() if d.type != 'pc'
        ]

        pc = [
            {
                "id": d.pk,
                "width": d.width or "",  
                "height": d.height or "",  
                "image": d.image or "",  
                "type": d.type or "",  
                "x": d.x or "",  
                "y": d.y or "",  
                "configuraciones": [
                        {
                            "ip": i.ip or "", 
                            "mascara": i.mask or "", 
                            "gateway": i.gateway or ""
                        }
                        for i in d.interfaces.all()
                    ][0]
                
            }
            for d in network.devices.all() if d.type == 'pc'
        ]

        dispositivos += pc
        
        cables = [
            {
                "from": {
                    "id": c.from_device.pk, 
                    "interface": c.from_interface or "", 
                    "x": c.from_x or "", 
                    "y": c.from_y or ""
                },
                "to": {
                    "id": c.to_device.pk, 
                    "interface": c.to_interface or "", 
                    "x": c.to_x or "", 
                    "y": c.to_y or ""
                },
                "peso": c.weight or ""
            }
            for c in Cable.objects.filter(from_device__network=network)
        ]
        
        data = {
            "id": network.pk,
            "nombre": network.name or "",
            "dispositivos": dispositivos,
            "cables": cables
        }
        
        return Response({
            "success": True,
            "data": data
        }, status=status.HTTP_200_OK)

    
    def post(self, request):
        name = request.data.get("nombre")
        if not name:
            return Response({
                "success": False,
                "data": {
                    "error": "FALTA NOMBRE"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Network.objects.create(user=request.user, name=name)

        return Response({
            "success": True, 
            "data": {
                "message": "Red creada correctamente"
            }
        }, status=status.HTTP_201_CREATED)
    
    
    def delete(self, request):
        pk= request.GET.get("id")
        print("AIOSJDFBIJAWBDIJHAWBD", pk)
        try:
            network = Network.objects.get(id=pk, user=request.user)
        except Network.DoesNotExist:
            return Response({
                "success": False,
                "data": {
                    "error": "RED NO ENCONTRADA"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        network.delete()
        return Response({
            "success": True, 
            "data": {
                "message": "Red eliminada correctamente"
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request):
        network_id = request.GET.get("id")
        if not network_id:
            return Response({
                "success": False,
                "data": {
                    "error": "Falta el ID de la red"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            network = Network.objects.get(id=network_id, user=request.user)
        except Network.DoesNotExist:
            return Response({
                "success": False,
                "data": {
                    "error": "RED NO ENCONTRADA"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Device.objects.filter(network=network).delete()
        Cable.objects.filter(from_device__network=network).delete()

        devices_data = request.data.get("dispositivos", [])
        cables_data = request.data.get("cables", [])
        devices_map = {}

        new_devices = []
        for d in devices_data:
            new_device = Device(
                network=network,
                width=d.get("width", 0),
                height=d.get("height", 0),
                image=d.get("image", ""),
                type=d.get("type", ""),
                x=d.get("x", 0),
                y=d.get("y", 0),
            )
            new_devices.append(new_device)

        devices = Device.objects.bulk_create(new_devices)


        for index, d in enumerate(devices_data):
            devices_map[d["id"]] = devices[index]

 
        new_interfaces = []
        new_routing_tables = []

        for d, device in zip(devices_data, devices):
            configuraciones = d.get("configuraciones", [{}])
            if isinstance(configuraciones, list) and len(configuraciones) > 0:
                configuraciones = configuraciones[0] 

            tipo = d.get("type")
            if tipo == 'pc':
                print(configuraciones)
                new_interfaces.append(Interface(
                    device=device,
                    name=configuraciones.get("nombre", ""),
                    ip=configuraciones.get("ip", ""),
                    mask=configuraciones.get("mascara", ""),
                    gateway=configuraciones.get("gateway", ""),
                ))
            else:
                interfaces = configuraciones.get("interfaces", []) if isinstance(configuraciones, dict) else []
                for i in interfaces:
                    print(i)
                    new_interfaces.append(Interface(
                        device=device,
                        name=i.get("nombre", ""),
                        ip=i.get("ip", ""),
                        mask=i.get("mascara", ""),
                        gateway=i.get("gateway", ""),
                    ))


                tabla = configuraciones.get("tabla", []) if isinstance(configuraciones, dict) else []
                for t in tabla:
                    new_routing_tables.append(RoutingTable(
                        device=device,
                        destiny=t.get("destino", ""),
                        destiny_mask=t.get("destinoMascara", ""),
                        jump=t.get("salto", ""),
                    ))

        Interface.objects.bulk_create(new_interfaces)
        RoutingTable.objects.bulk_create(new_routing_tables)

        new_cables = []
        for c in cables_data:
            new_cables.append(Cable(
                from_device=devices_map[c["from"]["id"]],
                from_interface=c["from"]["interface"],
                from_x=c["from"]["x"],
                from_y=c["from"]["y"],
                to_device=devices_map[c["to"]["id"]],
                to_interface=c["to"]["interface"],
                to_x=c["to"]["x"],
                to_y=c["to"]["y"],
                weight=c.get("peso", 0),
            ))

        Cable.objects.bulk_create(new_cables)

        return Response({
            "success": True, 
            "data": {
                "message": "Red actualizada correctamente"
            }
        }, status=status.HTTP_201_CREATED)

