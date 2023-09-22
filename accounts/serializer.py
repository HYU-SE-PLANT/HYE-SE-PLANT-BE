from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserCreateSerializer(serializers.Serializer):
    account_id = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
        
    def create(self, validated_data):
        user = User.objects.create( # User 생성
            account_id=validated_data['account_id'],
            user_name=validated_data['user_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserLoginSerializer(serializers.Serializer):
    account_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
        
    def validate(self, data):
        account_id = data.get("account_id", None)
        password = data.get("password", None)
        user = authenticate(account_id=account_id, password=password)
        
        if user is None:
            return {
                'account_id': 'None'
            }
        
        try:
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given account id and password does not exists'
            )
        return {
            'account_id': user.account_id,
            'token': {
                'access_token': access_token
            }
        }
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('account_id', 'user_name')
        read_only_fields = ('account_id',)