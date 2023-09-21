# 데이터 처리
from .serializer import *
from .models import User, Profile

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
                status=status.HTTP_409_CONFLICT
            )
        if serializer.validated_data['account_id'] == "None":
            return Response(
                {'message': 'fail'},
                status=status.HTTP_200_OK
            )
        else:
            response = {
                'account_id': serializer.data['account_id'],
                'success': True,
                'token': serializer.data['token']
            }
        return Response(response, status=status.HTTP_200_OK)


# 회원 정보 확인하기 view
# @permission_classes([IsAuthenticated])
# class UserMeAPIView(APIView):
#     # authentication 추가
#     authentication_classes = [BasicAuthentication, SessionAuthentication, JWTAuthentication]
#     def get(self, request, *args, **kwargs):
#         """
#         현재 로그인 된 유저의 모든 정보 반환
#         """
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             response = {
#                 'account_id': serializer.data['account_id'],
#                 'user_name': serializer.data['user_name']
#             }
#         return Response(response, status=status.HTTP_200_OK)


# 회원 정보 확인하기 view
@permission_classes([IsAuthenticated])
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # authentication 추가
    authentication_classes = [BasicAuthentication, SessionAuthentication, JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)