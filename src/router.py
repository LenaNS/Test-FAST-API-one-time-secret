from fastapi import APIRouter
from src.repository import SecretRepository


router = APIRouter(
    prefix=""
)


@router.post("/generate")
async def create_secret(secret: str, secret_phrase: str) -> dict:
    """Принимает secret и secret_phrase и отдает secret_key по которому этот secret можно получить.

    Args:
        secret (str): секрет
        secret_phrase (str): кодовая фраза

    Returns:
        dict: secret_key
    """
    secret_key = await SecretRepository.add_one(secret, secret_phrase)
    return {"secret_key": secret_key}


@router.get("/secrets/{secret_key}")
async def get_secret(secret_key: str, secret_phrase: str) -> dict:
    """Принимает на вход secret_key и secret_phrase и отдает secret

    Args:
        secret_key (str): секретный ключ
        secret_phrase (str): кодовая фраза

    Returns:
        dict: секрет
    """
    secret = await SecretRepository.get_secret(secret_key=secret_key, secret_phrase=secret_phrase)
    return {"secret": secret}
