import openai
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializer import ChatSerializer
from .models import Chat


@permission_classes([AllowAny])
class ChatGPTView(APIView):
    def get(self, request):
        openai.api_key = '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'
        serializer = ChatSerializer(data=request.query_params)
        
        if serializer.is_valid(raise_exception=True):
            prompt = serializer.validated_data['prompt']
            response = openai.Completion.create(
                engine = "gpt-4",
                prompt = prompt,
                max_tokens = 100
            )
            answer = response.choices[0].text
            
            # 데이터베이스에 저장
            Chat.objects.create(prompt=prompt, response=answer)
            
            return Response(
                {
                    "answer": answer
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )