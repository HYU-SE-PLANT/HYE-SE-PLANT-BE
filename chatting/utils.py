import openai
import requests
import random
from geopy.geocoders import Nominatim
from django.conf import settings
from django.shortcuts import get_object_or_404

from plants.models import Plant
from accounts.models import User
from .models import PlantReplier
from plants.serializer import PlantSerializer, PlantTypeSerializer

openai.api_key = settings.CHAT_GPT_API_KEY
weather_api_key = settings.WEATHER_API_KEY
geo_local = Nominatim(user_agent='South Korea')


# 주소 받아오기(위도, 경도)
def get_city_address(user_id):
    user = User.objects.get(id=user_id)
    address = user.address
    address_divided = address.split()
    address_input = ' '.join(address_divided[0:4])
    
    try:
        geo = geo_local(address_input)
        latitude, longitude = geo.latitude, geo.longitude
        print(latitude, longitude)
        return latitude, longitude
    except:
        return 0, 0


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


# 흙 상태 받아오기
def get_soil_condition():
    soil_condition = ["좋음", "나쁨"]
    selected_condition = random.choice(soil_condition)
    return selected_condition


# 채팅 응답 받아오기
def generate_chatgpt_response(user_chat_data, user_id, selected_date):
    # 식물 정보 가져오기
    plant_id = user_chat_data.get('plant_id')
    plant = get_object_or_404(Plant, pk=plant_id)
    plant_serializer = PlantSerializer(plant)
    plant_type_serializer = PlantTypeSerializer(plant.plant_type_id)
    
    # 흙 상태 가져오기
    soil_condition = get_soil_condition()
    
    # 날씨 정보 가져오기
    weather_data = get_weather_data(user_id)
    
    # 이전 대화 내용 불러오기
    chat_history = PlantReplier.objects.filter(
        plant_id=plant_id,
        created_at__date=selected_date
    ).order_by('created_at')
    
    if chat_history.exists():
        previous_messages = [
            {"role": "user" if chat.is_user_chat else "assistant", "content": chat.chatting_content}
            for chat in chat_history
        ]
    else:
        previous_messages = []
    
    prompt = f"식물 정보: {plant_serializer.data}, 식물 품종 정보: {plant_type_serializer.data}"
    prompt += f"\n현재 날씨: {weather_data['description']}, 온도: {weather_data['temperature']}°C, 습도: {weather_data['humidity']}."
    prompt += f"\n흙 상태: {soil_condition}"
    
    # 전송할 message 작성
    message_to_send = [
        {"role": "system", "content": f"You are a plant who receives the information from {prompt}. And you can answer freely, if you don't have any information. \
        You have to answer by comparing the current weather, temperature, and humidity. You also must say information about you smoothly. \
        You don't have to say the information of you when I don't ask you 'How are you today?'. You must answer by Korean."},
    ]
    message_to_send.extend(previous_messages)
    
    # 응답 받아오기
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_to_send
    )
    
    chatgpt_response = response['choices'][0]['message']['content']
    return {
        'chatting_content': chatgpt_response.strip(),
        'is_user_chat': False,
        'plant_id': plant_id
    }