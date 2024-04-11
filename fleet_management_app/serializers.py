from rest_framework import serializers

from .models import Taxis, Trajectories

class TaxisSerializer(serializers.ModelSerializer):
  class Meta:
    model = Taxis
    fields = '__all__'

class TrajectoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Trajectories
    fields = '__all__'