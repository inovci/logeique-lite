from django.urls import path
from .views import *

app_name = 'spaces'

urlpatterns = [
    path('', home, name='home'),
]
