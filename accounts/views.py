# 데이터 처리
from .serializer import *

# APIView 사용 관련
from rest_framework.views import APIView

# Response 관련
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# 인증 관련
import jwt
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from BloomMate_backend.settings import SECRET_KEY


# 회원가입 view
@permission_classes([AllowAny])
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Register success",
                },
                status=status.HTTP_200_OK
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     
# 로그인 view   
@permission_classes([AllowAny])
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(
            account_id=request.data.get("account_id"),
            password=request.data.get("password"),
        )
        
        if user is not None:
            serializer = UserSerializer(user)
            # 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            res = Response(
                {
                    "account_id": serializer.data['account_id'],
                    "user_name": serializer.data['user_name'],
                    "token": {
                        "access": access_token
                    },
                },
                status=status.HTTP_200_OK
            )
            
            # 토큰 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            return res
        else:
            return Response(
                {
                    "message": "User with given account id and password does not exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# 로그아웃 view
class LogOutAPIView(APIView):        
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {
                "message": "Logout success"
            },
            status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        return response


# 회원 정보 확인 및 수정하기 view
class UserInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        data = request.data # 수정할 정보가 들어있는 요청 데이터 가져오기
        
        # account_id를 변경하려고 할 때 에러 응답 반환
        if 'account_id' in data or len(data) > 1:
            return Response(
                {
                    "message": "아이디는 변경할 수 없습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # user_name을 빈칸으로 설정할 때 에러 응답 반환
        elif data['user_name'] == '':
            return Response(
                {
                    "message": "이름은 빈칸으로 설정할 수 없습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # 유효성 검사를 통해 user_name 필드만 변경 가능하도록 함
            serializer = UserSerializer(user, data=data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "account_id": serializer.data['account_id'],
                        "user_name": serializer.data['user_name'],
                        "date_joined": serializer.data['date_joined'],
                        "date_updated": serializer.data['date_updated'],
                    },                
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=400)