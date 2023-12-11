from narrator.service.llm_api import LLMInterface
from narrator.api.schemas import Narrator


class NarrationService:
    def __init__(self, api_client: LLMInterface):
        self.api_client = api_client

        self.narration_context = {
            'Morgan Freeman': "a drama movie",
            'Sir David Attenborough': "a nature documentary",
            'James Earl Jones': "a scene from Star Wars",
            'Vince Gilligan': "a director's commentary on a scene from Breaking Bad"
        }

    def narrate_image(self, b64_string: str, narrator: Narrator) -> str:
        narration_prompt = self.get_narration_instruction(narrator)
        return self.api_client.get_response_image(narration_prompt, b64_string)

    def narrate_image_stream(self, b64_string: str, narrator: Narrator):
        narrator_prompt = self.get_narration_instruction(narrator)
        return self.api_client.get_response_image_stream(narrator_prompt, b64_string)

    def get_narration_instruction(self, narrator: Narrator) -> str:
        return (f"You are {narrator}. Narrate the picture provided "
                f"as if it were {self.narration_context[narrator.value]}."
                f"Make it snarky and funny. Don't repeat yourself. Make it short. "
                f"If I do anything remotely interesting, make a big deal about it!")
