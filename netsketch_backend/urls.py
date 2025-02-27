from django.urls import path

from .views import *
from .endpoints import *

urlpatterns = []

#AUTH
authPatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterView.as_view(), name='register'),
]

urlpatterns += authPatterns 
#NETWORK
network_patterns = [
    path("network",NetworkView.as_view(), name ='network')
]
urlpatterns += network_patterns 


#USERDATA
user_patterns = [
    path("user",UserDetailView.as_view(), name ='user')
]
urlpatterns += user_patterns 

#USERNETWORKS
user_patterns = [
    path("user_networks",UserNetworksView.as_view(), name ='user_networks')
]
urlpatterns += user_patterns 


