import openai
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404

from plants.models import Plant
from accounts.models import User
from plants.serializer import PlantSerializer, PlantTypeSerializer

openai.api_key = settings.CHAT_GPT_API_KEY
weather_api_key = settings.WEATHER_API_KEY


# 주소 받아오기
def get_city_address(user_id):
    user = User.objects.get(id=user_id)
    address = user.address
    city_name = address.split()
    
    if any(suffix in city_name[0] for suffix in ["도"]):
        return city_name[1]
    else:
        return city_name[0]


# 날씨 데이터 받아오기
def get_weather_data(user_id):
    city_name = get_city_address(user_id)
    api_key = weather_api_key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") == 200:
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'city': data['name']
        }
        return weather
    else:
        return {'error': '날씨 정보를 찾을 수 없습니다.'}


def generate_chatgpt_response(user_chat_data, user_id):
    plant_id = user_chat_data.get('plant_id')
    plant = get_object_or_404(Plant, pk=plant_id)
    
    plant_serializer = PlantSerializer(plant)
    plant_type_serializer = PlantTypeSerializer(plant.plant_type_id)
    
    weather_data = get_weather_data(user_id)
    
    prompt = f"식물 정보: {plant_serializer.data}, 식물 품종 정보: {plant_type_serializer.data}"
    prompt += f"현재 날씨: {weather_data['description']}, 온도: {weather_data['temperature']}°C, 습도: {weather_data['humidity']}."
    input = f"사용자 질문: {user_chat_data['chatting_content']}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a plant who receives the information from prompt. And you can answer freely, if you don't have any information. \
                You have to answer by comparing the current weather, temperature, and humidity. You also must say information about you smoothly. You must answer by Korean."},
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": input}
        ]
    )
    
    chatgpt_response = response['choices'][0]['message']['content']
    return {
        'chatting_content': chatgpt_response.strip(),
        'is_user_chat': False,
        'plant_id': plant_id
    }