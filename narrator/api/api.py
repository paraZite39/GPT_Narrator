from starlette.responses import StreamingResponse

from narrator.app import app

from narrator.api.schemas import (
    NarrateRequestSchema,
    NarrateResponseSchema
)
from narrator.service.external_api import OpenAIAPI, ElevenLabsAPI
from narrator.service.narration import NarrationService
from narrator.service.repository import InMemoryUserRepository

USER_REPO = InMemoryUserRepository()


@app.post("/narrate", response_model=NarrateResponseSchema)
def narrate(request: NarrateRequestSchema):
    api_client = OpenAIAPI()
    narration_service = NarrationService(api_client)

    b64_string, narrator = request.b64_string, request.narrator

    if not b64_string.startswith("data:image/jpeg;base64,"):
        b64_string = f"data:image/jpeg;base64,{b64_string}"

    narration = narration_service.narrate_image(b64_string, narrator)
    return {'narration': narration}


@app.post("/narrate_stream")
async def narrate_stream(request: NarrateRequestSchema):
    text_client = OpenAIAPI(USER_REPO)
    audio_client = ElevenLabsAPI()
    narrator_service = NarrationService(text_client, audio_client)

    user_id, b64_string, narrator = request.user_id, request.b64_string, request.narrator.value

    if not b64_string.startswith("data:image/jpeg;base64,"):
        b64_string = f"data:image/jpeg;base64,{b64_string}"

    return StreamingResponse(narrator_service.narrate_image_audio_stream(user_id, b64_string, narrator),
                             media_type="audio/mpeg3")
