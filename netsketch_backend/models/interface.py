from django.db import models
from .device import Device

class Interface(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='interfaces')
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(blank=True, null=True)
    mask = models.GenericIPAddressField(blank=True, null=True)
    gateway = models.GenericIPAddressField(blank=True, null=True)
