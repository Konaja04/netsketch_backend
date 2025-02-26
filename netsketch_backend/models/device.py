from django.db import models
from .network import Network

class Device(models.Model):
    TIPO_CHOICES = [
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('pc', 'PC'),
    ]
    
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='devices')
    width = models.IntegerField()
    height = models.IntegerField()
    image = models.TextField()
    type = models.CharField(max_length=10, choices=TIPO_CHOICES)
    x = models.IntegerField()
    y = models.IntegerField()
    

