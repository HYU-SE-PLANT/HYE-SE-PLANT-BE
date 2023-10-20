import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ChatSerializer


def call_openai_api(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer YOUR_OPENAI_API_KEY',
        'Content-Type': 'application/json',
    }
    data = {
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    assistant_message = response.json()['choices'][0]['message']['content']
    return assistant_message


class ChatGPTView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']

            # API 호출
            gpt_response = call_openai_api(user_input)

            serializer.save(gpt_response=gpt_response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
