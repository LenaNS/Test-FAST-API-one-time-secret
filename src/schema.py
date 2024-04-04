from pydantic import BaseModel


class SSecretAdd(BaseModel):
    secret: bytes
    secret_phrase: str


class SSecret(SSecretAdd):
    secret_key: str