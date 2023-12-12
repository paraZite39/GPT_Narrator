from narrator.service.external_api import LLMInterface, AudioInterface
from narrator.api.schemas import Narrator


class NarrationService:
    def __init__(self, text_api_client: LLMInterface, audio_api_client: AudioInterface):
        self.api_client = text_api_client
        self.audio_client = audio_api_client

        self.narration_context = {
            'Morgan Freeman': "a drama movie",
            'Sir David Attenborough': "a nature documentary",
            'James Earl Jones': "a scene from Star Wars",
            'Vince Gilligan': "a director's commentary on a scene from Breaking Bad"
        }

    def narrate_image(self, b64_string: str, narrator: Narrator) -> str:
        narration_prompt = self.get_narration_instruction(narrator)
        return self.api_client.get_response_image(narration_prompt, b64_string)

    def narrate_image_stream(self, user_id: int, b64_string: str, narrator: Narrator):
        narrator_prompt = self.get_narration_instruction(narrator)
        return self.api_client.get_response_image_stream(user_id, narrator_prompt, b64_string)

    def narrate_image_audio_stream(self, user_id: int, b64_string: str, narrator: Narrator):
        narrator_prompt = self.get_narration_instruction(narrator)
        text = self.api_client.get_response_image(user_id, narrator_prompt, b64_string)
        return self.audio_client.get_audio(narrator, text)

    def get_narration_instruction(self, narrator: Narrator) -> str:
        return (f"You are {narrator}. Narrate the picture provided "
                f"as if it were {self.narration_context[narrator]}."
                f"Make it snarky and funny. Don't repeat yourself. Make it short. "
                f"If I do anything remotely interesting, make a big deal about it!")
