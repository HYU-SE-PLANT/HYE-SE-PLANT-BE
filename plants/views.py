from .models import *
from .serializer import *
from .utils import *

from rest_framework.response import Response
from rest_framework import status
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
        user = request.user
        
        plants = Plant.objects.filter(user_id=request.user) # 인증된 사용자의 식물만 확인
        plant_data = []
        
        for plant in plants:
            plant_info = PlantSerializer(plant).data
            plant_info['is_harvested'] = determine_is_harvested(plant.harvested_at)
            plant_info['growth_level'] = calculate_growth_level(plant.plant_type_id, plant.planted_at)
            plant_data.append(plant_info)
        
        response_data = {
            'DATA': plant_data,
            'garden_size': user.garden_size
        }
            
        return Response(response_data, status=status.HTTP_200_OK)
    

# 식물 세부정보 등록 - 백엔드에서 직접 추가(1순위)
class PlantType(APIView):
    permission_classes = [permissions.AllowAny] # 토큰 없이 누구나 세부정보 등록 가능
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = PlantTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# 등록한 식물의 세부 정보 확인(3순위)
class PlantDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

        
    # 식물 정보 자세히 보기
    def get(self, request, format=None):
        # account_id로 User 객체를 가져오기
        user = request.user
        plant_id = request.GET.get('plant_id', None)
        
        # User ID와 식물 id로 식물 조회
        plant = get_object_or_404(
            Plant.objects.select_related('plant_type_id'),
            user_id=user, id=plant_id
        )
        
        # 요청을 보낸 사용자가 식물의 소유자와 일치하는지 확인
        if request.user != user:
            return Response(
                {
                    'detail': '이 식물에 대한 접근 권한이 없습니다.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
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

        # 불필요한 정보 제거
        del plant_data['user_id']
        del plant_data['harvested_at']
        del plant_data['plant_type_id']

        return Response(plant_data, status=status.HTTP_200_OK)
    
    # 식물 수확하기
    def post(self, request, format=None):
        user = request.user
        plant_id = request.GET.get('plant_id', None)
        plant = get_object_or_404(Plant, user_id=user, id=plant_id)
        tmp_dict = {}
        harvested_at = request.data['harvested_at']
        
        tmp_dict['harvested_at']=harvested_at
        
        serializer = PlantSerializer(plant, data=tmp_dict, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # 식물 정보 수정하기
    def patch(self, request, format=None):
        # account_id로 User 객체를 가져오기
        user = request.user
        plant_id = request.GET.get('plant_id', None)
        
        # User ID와 식물 id로 식물 조회
        plant = get_object_or_404(Plant, user_id=user, id=plant_id)
        
        # 요청을 보낸 사용자가 식물의 소유자와 일치하는지 확인
        if request.user != user:
            return Response(
                {
                    'detail': '이 식물에 대한 접근 권한이 없습니다.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = PlantSerializer(plant, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            updated_plant = serializer.save()
            
            plant_type_serializer = PlantTypeSerializer(updated_plant.plant_type_id)
            
            # growth_level 계산
            growth_level = calculate_growth_level(updated_plant.plant_type_id, updated_plant.planted_at)

            response_data = {
                # 기존 Plant 필드
                'id': updated_plant.id,
                'plant_picture_url': updated_plant.plant_picture_url,
                'plant_nickname': updated_plant.plant_nickname,
                'planted_at': updated_plant.planted_at,
                # Plant_Type 데이터
                'plant_name': plant_type_serializer.data['plant_name'],
                'plant_temperature': plant_type_serializer.data['plant_temperature'],
                'plant_humidity': plant_type_serializer.data['plant_humidity'],
                'plant_illuminance': plant_type_serializer.data['plant_illuminance'],
                'plant_bloom_season': plant_type_serializer.data['plant_bloom_season'],
                'plant_watering_cycle': plant_type_serializer.data['plant_watering_cycle'],
                'plant_difficulty': plant_type_serializer.data['plant_difficulty'],
                'plant_caution': plant_type_serializer.data['plant_caution'],
                'germination_period_start': plant_type_serializer.data['germination_period_start'],
                'germination_period_end': plant_type_serializer.data['germination_period_end'],
                'growth_period_start': plant_type_serializer.data['growth_period_start'],
                'growth_period_end': plant_type_serializer.data['growth_period_end'],
                'harvest_period_start': plant_type_serializer.data['harvest_period_start'],
                'harvest_period_end': plant_type_serializer.data['harvest_period_end'],
                # 계산 결과
                'growth_level': growth_level
            }            
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 식물 삭제하기
    def delete(self, request, format=None):
        user = request.user
        plant_id = request.GET.get('plant_id', None)
        plant = get_object_or_404(Plant, user_id=user, id=plant_id)
        
        if not request.user == plant.user_id:
            return Response({
                "detail": "이 식물에 대한 접근 권한이 없습니다."
            },
            status=status.HTTP_403_FORBIDDEN
        )
            
        plant.delete()
        return Response({
            "message": "등록한 식물이 삭제되었습니다."
            },
            status=status.HTTP_200_OK
        )
    
    
# 식물 질병 목록 등록 - 백엔드에서 직접 추가
class PlantDiseaseTypeView(APIView):
    permission_classes = [permissions.AllowAny] # 토큰 없이 누구나 세부정보 등록 가능
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = PlantDiseaseTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# 식물 진단하기
class PlantDiseaseRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # 사진 촬용하여 AI로 판단하기
    def post(self, request):
        tmp_dict={}
        disease_id = resnet_AI_to_check_disease(request.data['diagnose_photo_url'])
        
        tmp_dict['disease_id']=str(disease_id)
        tmp_dict['plant_id']=Plant.objects.get(id=request.data['plant_id'] ).pk
        tmp_dict['diagnose_photo_url']=request.data['diagnose_photo_url']

        serializer = PlantDiseaseRecordSerializer(data=tmp_dict)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 진단 받은 리스트 불러오기 - 하나의 식물에 대해서 리스트 불러오기
    def get(self, request, format=None):
        plant_id = request.GET.get('plant_id', None)
        disease_data = Plant_Disease_Record.objects.filter(plant_id=plant_id, plant_id__user_id=request.user)
        plant_disease_data = []
        
        for data in disease_data:
            serialized_data = PlantDiseaseRecordSerializer(data).data
            plant = Plant.objects.get(id=data.plant_id.id)

            serialized_data['growth_level'] = calculate_growth_level(plant.plant_type_id, plant.planted_at)
            serialized_data['plant_disease_name'] = getPredictedName(int(serialized_data['disease_id']))
            plant_disease_data.append(serialized_data)
            serialized_data.pop('plant_id', None)
            serialized_data.pop('disease_id', None)
        
        response_data = {
            'DATA': plant_disease_data,
            'plant_nickname': plant.plant_nickname
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
# 식물 진단한 기록 상세히 보기
class PlantDiseaseRecordDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        disease_record_id = request.GET.get('disease_record_id', None)
        
        disease_record = Plant_Disease_Record.objects.get(id=disease_record_id)
        serialized_data = PlantDiseaseRecordSerializer(disease_record).data
        
        plant = Plant.objects.get(id=disease_record.plant_id.id)
        disease_type = Plant_Disease_Type.objects.get(id=disease_record.disease_id.id)
        plant_name = plant.plant_type_id.plant_name
        
        serialized_data['plant_name'] = plant_name
        serialized_data['growth_level'] = calculate_growth_level(plant.plant_type_id, plant.planted_at)
        serialized_data['plant_disease_name'] = getPredictedName(int(serialized_data['disease_id']))
        serialized_data['plant_disease_symptom'] = disease_type.plant_disease_symptom
        serialized_data['plant_disease_condition'] = disease_type.plant_disease_condition
        serialized_data['plant_nickname'] = plant.plant_nickname
        serialized_data.pop('plant_id', None)
        serialized_data.pop('disease_id', None)
        
        return Response(serialized_data, status=status.HTTP_200_OK)