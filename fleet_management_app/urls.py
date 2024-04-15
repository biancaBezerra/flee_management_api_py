from django.contrib import admin
from django.urls import include, path


from . import views


urlpatterns = [
    path('taxis/', views.get_taxis, name='get_all_taxis'),
    path('trajectories/', views.get_trajectories, name='get_all_trajectories'),
]
