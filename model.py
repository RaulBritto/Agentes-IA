from pydantic import BaseModel


class PersonalAssistant(BaseModel):
    topic: str
    answer: str
    sources: list[str]
    tools_used: list[str]
