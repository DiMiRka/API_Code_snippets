from pydantic import BaseModel


class SnippetsCode(BaseModel):
    id: int
    code: str
    user_id: int


class SnippetCreate(BaseModel):
    text: str
