from cinema_booking.serializers import BookSeatSerializer
# CORREÇÃO: Importar explicitamente
from .models import Notification
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):
    seat = BookSeatSerializer()
    class Meta:
        model = Notification
        fields = '__all__'