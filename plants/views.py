from .models import *
from .serializer import *
from .utils import determine_is_harvested, calculate_growth_level

from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

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
        