from django.contrib import admin
from .models import Taxis, Trajectories

# Register your models here.

admin.site.register(Taxis)
admin.site.register(Trajectories)
