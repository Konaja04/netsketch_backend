from django.contrib import admin
from .models import * 
# Register your models here.


admin.site.register(User)
admin.site.register(Network)
admin.site.register(Device)
admin.site.register(Cable)
admin.site.register(Interface)
admin.site.register(RoutingTable)