import openai
from django.conf import settings


openai.api_key = settings.CHAT_GPT_API_KEY

def send_sentence_to_api(sentence):
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "너는 올해 9월에 심겨진 딸기 모종이야."
            },
            {
                "role": "assistant",
                "content": "너는 레드펄 품종이야. 주변 온도는 17도에서 18도를 왔다갔다 해. 조금 습한 상태야. 너가 심겨져있는 토양은 배수가 잘되고 보수력이 있는 양토야. 토양의 산도는 약산성이야. 땅의 온도는 20도야."
            },
            {
                "role": "user",
                "content": f"{sentence}"
            },
        ],
    )
    return res["choices"][0]["message"]["content"]


# assistant로 설정해둬야 앞서서 이야기 한 내용과 같이 이어서 계속 대화를 이어나갈 수 있음