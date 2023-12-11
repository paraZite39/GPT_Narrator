from openai import OpenAI, AsyncOpenAI


class LLMInterface:
    def get_response(self, system_messages: list, user_messages: str):
        raise NotImplementedError

    def get_response_image(self, instruction: str, image_url: str):
        raise NotImplementedError

    def get_response_image_stream(self, instruction: str, image_url: str):
        raise NotImplementedError


class OpenAIAPI(LLMInterface):
    def __init__(self):
        self.openai_client = OpenAI()

    def get_response(self, system_messages: list, user_message: str) -> str:
        messages = self._build_messages(system_messages, user_message)
        response = self.openai_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages
        )
        return response.choices[0].message.content

    @staticmethod
    def _build_messages(system_messages: list, user_message: str = None) -> list:
        messages = [{'role': 'system', 'content': message} for message in system_messages]

        if user_message:
            messages.append({'role': 'user', 'content': user_message})

        return messages

    def get_response_image(self, instruction: str, image_url: str) -> str:
        messages = self._build_messages_image(instruction, image_url)
        response = self.openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=1200
        )
        return response.choices[0].message.content

    def get_response_image_stream(self, instruction: str, image_url: str):
        messages = self._build_messages_image(instruction, image_url)
        response = self.openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=1200,
            stream=True
        )

        for event in response:
            current_response = event.choices[0].delta.content
            if current_response:
                yield current_response

    @staticmethod
    def _build_messages_image(instruction: str, image_url: str) -> list:
        return [
            {'role': 'user',
             'content': [
                 {'type': 'text', 'text': instruction},
                 {'type': 'image_url',
                  'image_url': {
                      'url': image_url,
                  }}
             ]}
        ]
