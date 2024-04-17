from rest_framework import serializers
from .models import Taxis, Trajectories
class TaxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxis
        fields = ['id', 'plate']  # Inclua todas as informações do táxi que você deseja retornar
class TrajectoriesSerializer(serializers.ModelSerializer):
    taxi = TaxisSerializer()  # Use o serializer do táxi para serializar o objeto de táxi
    class Meta:
        model = Trajectories
        fields = '__all__'