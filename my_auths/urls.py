from django.urls import path
from .views import *

app_name = 'my_auths'

urlpatterns = [
    # -------------------------------------------------Auths urls-------------------------------------------------
    path('login/', login, name='login'),
    path('aut_login/', aut_login, name='aut_login'),
    path('register/', register, name='register'),
    path('space/', user_space, name='space'),
    path('logout/', logout, name='logout'),
    # -------------------------------------------------Landlord urls----------------------------------------------
    path('update-landlord-profile/', updateLandlordProfile, name='updateLandlordProfile'),
    path('landlord/', landlordClients, name='landlordClients'),
    path('maisons/', landlordMaisons, name='landlordMaisons'),
    path('add-maison/', addMaison, name='addMaison'),
    path('delete-maison/<int:id>', deleteMaison, name='deleteMaison'),
    path('edit-maison/<int:id>', editMaison, name='editMaison'),
]
