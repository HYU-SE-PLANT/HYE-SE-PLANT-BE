from .models import Community
from .serializer import CommunitySerializer

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


# Community에 올라온 질문 목록 보여주기
class QuestionList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 질의응답 리스트 보여줄 때
    def get(self, request):
        questions = Community.objects.all()
        serializer = CommunitySerializer(questions, many=True)
        return Response(serializer.data)