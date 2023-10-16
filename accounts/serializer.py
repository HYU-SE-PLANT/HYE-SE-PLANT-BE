from .models import User
from rest_framework import serializers
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        user = User.objects.create_user(
            account_id = validated_data['account_id'],
            user_name = validated_data['user_name'],
            tiiun_number=validated_data['tiiun_number'],
            cultivation_experience=validated_data['cultivation_experience'],
            garden_size=validated_data['garden_size'],
            address=validated_data['address'],
            password = validated_data['password']
        )
        return user