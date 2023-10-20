from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import PlantChatSerializer


class PlantChattingView(APIView):
    serializer_class = PlantChatSerializer
    
    def get(self, request, format=None):
        pass
    
    def post(self, request, format=None):
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)