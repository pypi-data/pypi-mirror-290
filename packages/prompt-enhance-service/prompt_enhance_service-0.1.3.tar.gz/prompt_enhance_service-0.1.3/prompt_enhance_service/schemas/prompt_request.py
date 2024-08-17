from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    customization: Optional[bool] = None
    domain: Optional[str] = None
