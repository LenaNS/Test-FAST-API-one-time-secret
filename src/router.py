from fastapi import APIRouter, Depends
from src.schema import SSecretAdd
from typing import Annotated
from src.repository import SecretRepository


router = APIRouter(
    prefix=""
)


@router.post("/generate")
async def get_secret(secret: str, secret_phrase: str) -> dict:
    secret_key = await SecretRepository.add_one(secret, secret_phrase)
    return {"secret_key": secret_key}


@router.get("/secrets/{secret_key}")
async def get_secret(secret_key: str, secret_phrase: str) -> dict:
    secret = await SecretRepository.get_secret(secret_key=secret_key, secret_phrase=secret_phrase)
    return {"secret": secret}
