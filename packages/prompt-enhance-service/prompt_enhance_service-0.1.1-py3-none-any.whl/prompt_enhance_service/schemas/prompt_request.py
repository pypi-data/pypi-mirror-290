from pydantic import BaseModel

class PromptRequest(BaseModel):
    message: str
    session_id: str
    customization: bool
    domain: str
