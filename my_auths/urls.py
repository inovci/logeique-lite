from django.urls import path
from .views import *

app_name = 'my_auths'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('space/', user_space, name='space'),
    path('logout/', logout, name='logout'),
]
