from .models import *
from rest_framework import serializers


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_Type
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    # account_id 받아올 것
    user_id = serializers.ReadOnlyField(source = 'user_id.account_id')
    
    class Meta:
        model = Plant
        fields = '__all__'
        