
from django.db import models
from .user import User

class Network(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)