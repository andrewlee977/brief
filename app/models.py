from pydantic import BaseModel
from typing import Optional

class NewsBriefing(BaseModel):
    summary: str
    audio_content: bytes 