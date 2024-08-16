from pydantic import BaseModel

class DomainQuestions(BaseModel):
    domain : str
    questions : list
