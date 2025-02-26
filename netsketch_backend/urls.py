from django.urls import path

from .views import *
from .endpoints import *
urlpatterns = []

#AUTH
authPatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterView.as_view(), name='register'),

#     path('auth/passwordReset', AuthView.as_view(), name = 'change-password'),
#     path('auth/sendVerification', AuthView.as_view(), name = 'send-verification'),
]

urlpatterns += authPatterns 



