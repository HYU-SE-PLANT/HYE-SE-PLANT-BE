from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user_input', 'gpt_response']