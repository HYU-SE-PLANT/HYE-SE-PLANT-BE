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