from .models import Article
from .serializer import ArticleSerializer

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


# Article을 띄워서 보여주기
class ArticleList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # Article 목록 불러오기
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        response_data = {
            'DATA': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

# Article 등록하기 - 백엔드에서 직접 넣어줄 예정
class ArticleCreate(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)