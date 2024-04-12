from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer

import json


@api_view(['GET'])
def get_taxis(request):
    if request.method == 'GET':
        taxis = Taxis.objects.all()                          # Get all objects in Tax's database (It returns a queryset)
        serializer = TaxisSerializer(taxis, many=True)       # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)
        return Response(serializer.data)                     # Return the serialized data
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_trajectories(request):
    if request.method == 'GET':
        trajectories = Trajectories.objects.all()
        serializer = TrajectoriesSerializer(trajectories, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# def databaseEmDjango():
#     data = User.objects.get(pk='gabriel_nick')          # OBJETO
#     data = User.objects.filter(user_age='25')           # QUERYSET
#     data = User.objects.exclude(user_age='25')          # QUERYSET
#     data.save()
#     data.delete()