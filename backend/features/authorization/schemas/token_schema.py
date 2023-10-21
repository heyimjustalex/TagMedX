from pydantic import BaseModel


class TokenRsponse(BaseModel):
    access_token: str
    token_type: str
