from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # CORREÇÃO: Usamos '__all__' para evitar erros de digitação de campos
        fields = '__all__'
        # Ocultamos a senha para segurança
        extra_kwargs = {'password': {'write_only': True}}