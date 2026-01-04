from rest_framework import serializers
from managecinema.serializers import CinemaDeckSerializer
# CORREÇÃO: Importar explicitamente os modelos usados
from .models import AvailableSlots, Seat 

class AvailableSlotsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlots
        fields = '__all__'
        depth = 2

class SeatSerializer(serializers.ModelSerializer):
    deck = CinemaDeckSerializer()
    class Meta:
        model = Seat
        fields = '__all__'
        depth = 1