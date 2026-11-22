"""
Аутентификация запросов по JWT, выданному сервисом авторизации.

Backend больше не хранит пользователей и не обращается к сервису авторизации
на каждый запрос: он лишь проверяет подпись токена общим секретом JWT_SECRET.
"""

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication


class TokenUser:
    """Пользователь, восстановленный из содержимого JWT (без обращения к БД)."""

    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, payload: dict):
        self.id = self.pk = int(payload["sub"])
        self.username = payload.get("username", "")
        self.is_staff = bool(payload.get("is_staff", False))

    def __str__(self):
        return self.username


class JWTCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            # просроченный или поддельный токен — запрос обрабатывается как анонимный
            return None
        return TokenUser(payload), token
