# 데이터 처리
from .serializer import *
from .models import User

# APIView 사용 관련
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# 인증 관련
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


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
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            response = {
                'account_id': serializer.validated_data['account_id'],
                'success': True,
                'token': serializer.validated_data['token']
            }
        return Response(response, status=status.HTTP_200_OK)


# 회원 정보 확인 및 수정하기 view
@permission_classes([IsAuthenticated])
class UserInfoUpdateAPIView(APIView):
    # authentication 추가
    authentication_classes = [BasicAuthentication, SessionAuthentication, JWTAuthentication]

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
                {"message": "아이디는 변경할 수 없습니다."}, status=400
            )
        # user_name을 빈칸으로 설정할 때 에러 응답 반환
        elif data['user_name'] == '':
            return Response(
                {"message": "이름은 빈칸으로 설정할 수 없습니다."}, status=400
            )
        else:
            # 유효성 검사를 통해 user_name 필드만 변경 가능하도록 함
            serializer = UserSerializer(user, data=data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)