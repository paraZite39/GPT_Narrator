from starlette.responses import StreamingResponse

from narrator.app import app

from narrator.api.schemas import (
    NarrateRequestSchema,
    NarrateResponseSchema
)
from narrator.service.llm_api import OpenAIAPI
from narrator.service.narration import NarrationService


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
    api_client = OpenAIAPI()
    narrator_service = NarrationService(api_client)

    b64_string, narrator = request.b64_string, request.narrator

    if not b64_string.startswith("data:image/jpeg;base64,"):
        b64_string = f"data:image/jpeg;base64,{b64_string}"

    return StreamingResponse(narrator_service.narrate_image_stream(b64_string, narrator),
                             media_type="text/event-stream")