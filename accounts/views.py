from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import *
from .models import User
from rest_framework import status
from rest_framework.response import Response
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


@permission_classes([IsAuthenticated])
class UserUpdateAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JWTAuthentication]
    # 특정 정보를 들고오는 API
    def get(self, request, unique):
        userInfo = self.get_object(unique=unique)
        serializer = UserInfoSerializer(userInfo)
        return Response(serializer.data)