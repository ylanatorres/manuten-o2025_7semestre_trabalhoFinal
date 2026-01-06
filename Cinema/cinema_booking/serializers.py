from rest_framework import serializers
from managecinema.serializers import CinemaDeckSerializer
# Importamos todos os modelos necessários
from .models import AvailableSlots, Seat, BookSeat, SeatManager

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

class BookSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSeat
        fields = '__all__'

# --- A CLASSE QUE FALTOU DESSA VEZ ---
class SeatManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatManager
        fields = '__all__'