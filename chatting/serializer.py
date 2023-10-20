from rest_framework import serializers

from .models import PlantReplier
from .utils import send_sentence_to_api


class PlantChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantReplier
        fields = ("id", "input_text", "output_text")
        extra_kwargs = {
            "output_text": {"read_only":True}
        }
        
    def create(self, validated_data):
        output_text = send_sentence_to_api(validated_data['input_text'])
        instance = PlantReplier(input_text=validated_data['input_text'], output_text=output_text)
        instance.save()
        return instance