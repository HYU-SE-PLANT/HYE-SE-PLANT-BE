from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import PlantChatSerializer
from .models import PlantReplier
from accounts.models import User
from plants.models import Plant
from .utils import generate_chatgpt_response

from django.utils import timezone


# def get_weather_data(address):


class PlantChattingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 채팅 불러오기
    def get(self, request, format=None):
        user = request.user
        plant_id = request.GET.get('plant_id', None)
        date_str = request.GET.get('date', None)
        date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        chat_records = PlantReplier.objects.filter(
            plant_id = plant_id,
            created_at__date = date_obj,
            plant_id__user_id = user.id
        )
        serializer = PlantChatSerializer(chat_records, many=True)
        
        plant = Plant.objects.get(id=plant_id)
        plant_nickname = plant.plant_nickname
        
        response_data = {
            'DATA': [{
                'id': chat['id'],
                'chatting_content': chat['chatting_content'],
                'is_user_chat': chat['is_user_chat'],
                'created_at': chat['created_at']
            } for chat in serializer.data],
            'plant_nickname': plant_nickname
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    
    # 채팅하기
    def post(self, request, format=None):
        user_id = request.user.id
        plant_id = request.GET.get('plant_id', None)
        selected_date = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
        is_user_chat = request.data.get('is_user_chat', True)
        current_date = timezone.now().date()
        
        if timezone.datetime.strptime(selected_date, '%Y-%m-%d').date() != current_date:
            return Response({"error": "오늘 날짜가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 사용자 입력 처리
        if is_user_chat:
            user_chat_data = request.data
            user_chat_data['plant_id'] = plant_id
            user_chat_data['is_user_chat'] = True
            serializer = PlantChatSerializer(data=user_chat_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                chatgpt_response = generate_chatgpt_response(serializer.data, user_id, selected_date)
                
                # chatgpt 응답 저장
                response_serializer = PlantChatSerializer(data=chatgpt_response)
                if response_serializer.is_valid(raise_exception=True):
                    response_serializer.save()
                
                return Response(chatgpt_response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # chatgpt 응답 처리
        else:
            chatgpt_data = request.data
            chatgpt_data['plant_id'] = plant_id
            serializer = PlantChatSerializer(data=chatgpt_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# postman으로 확인하는 방법
# JWT token과 chatGPT api token 2가지를 동시에 사용해야 함
# postman의 Authorization 부분에 Bearer로 설정 후, JWT token을 삽입
# postman의 Headers 부분에 Key: Authorization, Value: Bearer [chatGPT api token]을 넣음으로써 작동 가능 확인
# 단, 현재 테스트 형식으로 작성한 내용은 로그인 한 사람이 A, A가 생성한 식물이 B라는 것을 모두 배제한 채,
# get method로는 모든 사람의 질문 내용을 불러온다는 한계가 있음
# filter 기능을 이용해 model에 작성자와 해당 식물 정보까지 추가를 하여 작업이 진행되어야 할 것으로 판단