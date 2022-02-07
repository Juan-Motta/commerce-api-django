from rest_framework import serializers

from .models import Profile

class ProfiletListSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para listar los perfiles
    """
    class Meta:
        model = Profile
        fields = ['id', 'name']
    
class ProfileCreateSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para crear y actualizar los perfiles
    """
    class Meta:
        model = Profile
        fields = ['name']
    