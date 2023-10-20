from rest_framework import serializers

from .models import PlantReplier
from .utils import send_sentence_to_api


class PlantChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantReplier
        fields = ("id", "user_input", "chatgpt_output")
        extra_kwargs = {
            "chatgpt_output": {"read_only":True}
        }
        
    def create(self, validated_data):
        chatting = PlantChatSerializer(**validated_data)
        chatgpt_output = send_sentence_to_api(validated_data['user_input'])
        chatting.chatgpt_output = chatgpt_output
        chatting.save()
        return chatting