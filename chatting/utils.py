import openai
from django.conf import settings


openai.api_key = settings.CHAT_GPT_API_KEY

def send_sentence_to_api(sentence):
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "assistant",
                "content": f"{sentence}"
            },
        ],
    )
    return res["choices"][0]["message"]["content"]


# assistant로 설정해둬야 앞서서 이야기 한 내용과 같이 이어서 계속 대화를 이어나갈 수 있음