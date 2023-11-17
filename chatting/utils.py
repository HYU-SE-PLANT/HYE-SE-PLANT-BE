import openai
from django.conf import settings
from django.shortcuts import get_object_or_404

from plants.models import Plant
from plants.serializer import PlantSerializer, PlantTypeSerializer

openai.api_key = settings.CHAT_GPT_API_KEY


def generate_chatgpt_response(self, user_chat_data):
    plant_id = user_chat_data.get('plant_id')
    plant = get_object_or_404(Plant, pk=plant_id)
    
    plant_serializer = PlantSerializer(plant)
    plant_type_serializer = PlantTypeSerializer(plant.plant_type_id)
    
    prompt = f"식물 정보: {plant_serializer.data}, 식물 품종 정보: {plant_type_serializer.data}, 사용자 질문: {user_chat_data['chatting_content']}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        message=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    chatgpt_response = response['choices'][0]['message']['content']
    return {
        'chatting_content': chatgpt_response.strip(),
        'is_user_chat': False,
        'plant_id': plant_id
    }