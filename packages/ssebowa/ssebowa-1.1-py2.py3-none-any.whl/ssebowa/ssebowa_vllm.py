import base64
import requests

class ssebowa_vllm:
    def __init__(self):
        self.api_key = "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"
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key }"
        }

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def understand(self, image_path, text):
        base64_image = self.encode_image(image_path)

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(self.base_url, headers=self.headers, json=payload)

        return response.json()