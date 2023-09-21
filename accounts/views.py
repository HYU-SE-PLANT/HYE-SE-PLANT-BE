# 데이터 처리
from .serializer import *
from .models import User

# APIView 사용 관련
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from django.core import exceptions

# 인증 관련
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateAPIView


# Create your views here.
# 회원가입 view
@permission_classes([AllowAny])
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        
     
# 로그인 view   
@permission_classes([AllowAny])
class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {'message': 'Request Body Error.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.validated_data['account_id'] == "None":
            return Response(
                {'message': 'Authentication fail'},
                status=status.HTTP_200_OK
            )
        else:
            response = {
                'account_id': serializer.validated_data['account_id'],
                'success': True,
                'token': serializer.validated_data['token']
            }
        return Response(response, status=status.HTTP_200_OK)


# 회원 정보 확인하기 view
@permission_classes([IsAuthenticated])
class UserInfoUpdateAPIView(APIView):
    # authentication 추가
    authentication_classes = [BasicAuthentication, SessionAuthentication, JWTAuthentication]

    def get(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        data = request.data # 수정할 정보가 들어있는 요청 데이터 가져오기
        
        # account_id 고정시키기
        data['account_id'] = user.account_id
        serializer = UserSerializer(user, data=data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)