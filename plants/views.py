from .models import *
from .serializer import *
from .utils import determine_is_harvested, calculate_growth_level

from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


# 등록한 Plant 목록 보여주기
class PlantList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        plants = Plant.objects.filter(user_id=request.user) # 인증된 사용자의 식물만 확인
        plant_data = []
        
        for plant in plants:
            plant_info = PlantSerializer(plant).data
            plant_info['is_harvested'] = determine_is_harvested(plant.harvested_at)
            plant_info['growth_level'] = calculate_growth_level(plant.plant_type_id, plant.planted_at)
            plant_data.append(plant_info)
            
        return Response(plant_data, status=status.HTTP_200_OK)
    
    # TODO: API 명세서 - {[식물 정보], garden_size: 0} 와 같이 garden_size를 식물 정보 외곽에 나타낼 수 있게 하기
    

# 식물 세부정보 등록 - 백엔드에서 직접 넣기(1순위)
class PlantType(APIView):
    permission_classes = [permissions.AllowAny] # 토큰 없이 누구나 세부정보 등록 가능
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = PlantTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: 현재 토마토 정보만 들어가 있음. 기타 작물 정보도 추가할 것


# 새로운 식물 등록(2순위)
class PlantCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] # 가입한 사람만이 등록 가능
    
    def post(self, request):
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: garden_size와 연계하여, 식물 등록 일정 개수 넘기지 않도록 설정하기
    

# 등록한 식물의 세부 정보 확인(3순위)
class PlantDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
        
    # 식물 정보 자세히 보기
    def get(self, request, pk, format=None):
        # select_related: Plant와 연관된 Plant_Type 정보를 함께 가져온다.
        plant = get_object_or_404(Plant.objects.select_related('plant_type_id'), pk=pk)
        
        plant_serializer = PlantSerializer(plant)        
        plant_data = plant_serializer.data # Plant 데이터 가져오기
        
        # Plant_Type 데이터 가져오기
        plant_type = plant.plant_type_id
        plant_data.update({
            'plant_name': plant_type.plant_name,
            'plant_temperature': plant_type.plant_temperature,
            'plant_humidity': plant_type.plant_humidity,
            'plant_illuminance': plant_type.plant_illuminance,
            'plant_bloom_season': plant_type.plant_bloom_season,
            'plant_watering_cycle': plant_type.plant_watering_cycle,
            'plant_difficulty': plant_type.plant_difficulty,
            'plant_caution': plant_type.plant_caution,
            'germination_period_start': plant_type.germination_period_start,
            'germination_period_end': plant_type.germination_period_end,
            'growth_period_start': plant_type.growth_period_start,
            'growth_period_end': plant_type.growth_period_end,
            'harvest_period_start': plant_type.harvest_period_start,
            'harvest_period_end': plant_type.harvest_period_end,
        })
        
        # growth_level 계산
        plant_data['growth_level'] = calculate_growth_level(plant.plant_type_id, plant.planted_at)

        del plant_data['user_id']
        del plant_data['harvested_at']
        del plant_data['plant_type_id']

        return Response(plant_data, status=status.HTTP_200_OK)