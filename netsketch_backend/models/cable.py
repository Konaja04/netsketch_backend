
from django.db import models
from .device import Device

class Cable(models.Model):

    from_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='cables_salida')
    from_interface = models.CharField(max_length=50)
    from_x = models.IntegerField()
    from_y = models.IntegerField()
    
    to_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='cables_entrada')
    to_interface = models.CharField(max_length=50)
    to_x = models.IntegerField()
    to_y = models.IntegerField()
    
    weight = models.IntegerField()