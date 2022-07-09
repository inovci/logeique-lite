from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Maison)
admin.site.register(Landlord)
admin.site.register(Client)
admin.site.register(Proposal)
