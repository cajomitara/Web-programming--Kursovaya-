"""Выпуск и проверка JWT-токенов доступа."""

import time

import jwt
from django.conf import settings

ALGORITHM = "HS256"


def issue_token(user) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user.id),          # идентификатор пользователя (строкой, как требует стандарт JWT)
        "username": user.username,
        "is_staff": user.is_staff,
        "iat": now,
        "exp": now + settings.JWT_LIFETIME_SECONDS,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Возвращает содержимое токена или бросает jwt.InvalidTokenError."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
