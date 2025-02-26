from django.db import models
from .device import Device

class RoutingTable(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="routing_tables")
    destiny = models.GenericIPAddressField()
    destiny_mask = models.GenericIPAddressField()
    jump = models.GenericIPAddressField()