from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

from random import choice
from string import ascii_letters, digits


SHORT_URL_SIZE = 20
AVAILABLE_CHARS = ascii_letters + digits


def secret_key_generator():
        url = ''
        for i in range(SHORT_URL_SIZE):
             url += choice(AVAILABLE_CHARS)
        return url


class Model(DeclarativeBase):
    pass


class SecretsOrm(Model):
    __tablename__ = "secrets"

    secret_key: Mapped[str] = mapped_column(String(SHORT_URL_SIZE), primary_key=True, default=secret_key_generator)
    secret: Mapped[bytes]
    secret_phrase: Mapped[str]