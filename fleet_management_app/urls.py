from django.urls import path

from .views import viewsTaxis, viewsTrajectories, viewsLastLocation

urlpatterns = [
    path('taxis/', viewsTaxis.get_taxis, name='get_all_taxis'),
    path('trajectories/', viewsTrajectories.get_trajectories, name='get_all_trajectories'),
    path('lastlocation/', viewsLastLocation.get_last_location, name='find_last_trajectories'),
]
