import requests
from enum import Enum


class OpenAI:
    API_KEY = None

    def __init__(self, api_key: str) -> None:
        self.API_KEY = api_key

    class Models(Enum):
        DAVINCI = 'text-davinci-003'
        CURIE = 'text-curie-001'
        BABBAGE = 'text-babbage-001'
        ADA = 'text-ada-001'

    def make_request(self, prompt: str, max_tokens: int = 128, temperature: float = 0, model: Models = Models.DAVINCI) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.API_KEY}'
        }
        data = {
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'model': 'text-davinci-003',
        }
        request = requests.post(
            'https://api.openai.com/v1/completions', json=data, headers=headers)
        text = request.text
        print(text)
        data = request.json()
        print(data)
        answer = data['choices'][0]['text']
        print(answer)
        return answer
