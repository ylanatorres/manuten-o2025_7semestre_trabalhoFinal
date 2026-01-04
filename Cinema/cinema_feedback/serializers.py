from rest_framework import serializers
# --- CORREÇÃO: Importar apenas Review ---
from .models import Review 

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"