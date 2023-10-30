from pydantic import BaseModel


class TokenCreate(BaseModel):
    email: str
    password: str
