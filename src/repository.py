from src.database import session_local
from src.schema import SSecretAdd
from src.models import SecretsOrm
from sqlalchemy import select, and_
import hashlib
from cryptography.fernet import Fernet


SALT = "test"
CODER = Fernet(b'gHXY2sgsp-WanAEhugFf9R9LoFS5ZPZLSSsTjG8sdqM=')


class SecretRepository: 
    @classmethod
    async def add_one(cls, secret: str, secret_phrase: str) -> str:
        async with session_local() as session:
            secret_phrase = hashlib.pbkdf2_hmac(hash_name='sha256', password=secret_phrase.encode(), salt=SALT.encode(), iterations=100000).hex()
            secret = CODER.encrypt(secret.encode())
            one_secret = SecretsOrm(secret=secret, secret_phrase=secret_phrase)
            session.add(one_secret)
            await session.flush()
            await session.commit()
            return one_secret.secret_key
        
    # @classmethod
    # async def delete_secret(cls, secret_key: str, secret_phrase: str) -> str:
    #     async with session_local() as session:
    #         return None
        
    @classmethod
    async def get_secret(cls, secret_key: str, secret_phrase: str) -> str:
        async with session_local() as session:
            secret_phrase = hashlib.pbkdf2_hmac(hash_name='sha256', password=secret_phrase.encode(), salt=SALT.encode(), iterations=100000).hex()
            query = select(SecretsOrm).where(and_(SecretsOrm.secret_key == secret_key, SecretsOrm.secret_phrase == secret_phrase))
            result = await session.execute(query)
            secret = result.scalars().first()
            if secret is None:
                return None
            await session.delete(secret)
            await session.flush()
            await session.commit()
            return CODER.decrypt(secret.secret)
        