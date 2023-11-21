from rest_framework import serializers

from .models import PlantReplier
from plants.serializer import PlantSerializer, PlantTypeSerializer
# from .utils import send_sentence_to_api


class PlantChatSerializer(serializers.ModelSerializer):
    plant_info = serializers.SerializerMethodField()
    plant_type_info = PlantTypeSerializer(source='plant_id.plant_type_id', read_only=True)
    
    class Meta:
        model = PlantReplier
        fields = ['id', 'chatting_content', 'is_user_chat', 'created_at', 'plant_id', 'plant_info', 'plant_type_info']
        
    def get_plant_info(self, obj):
        # Plant 모델에 대한 정보를 반환하는 메서드
        plant = obj.plant_id
        return PlantSerializer(plant).data