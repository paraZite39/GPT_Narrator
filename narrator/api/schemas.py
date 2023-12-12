from enum import Enum

from pydantic import BaseModel


class Narrator(Enum):
    morgan_freeman = "Morgan Freeman"
    david_attenborough = "Sir David Attenborough"
    james_earl_jones = "James Earl Jones"
    vince_gilligan = "Vince Gilligan"


class NarrateRequestSchema(BaseModel):
    user_id: int
    b64_string: str
    narrator: Narrator


class NarrateResponseSchema(BaseModel):
    narration: str
