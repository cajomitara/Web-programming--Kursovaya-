"""
Клиент внутреннего API сервиса авторизации.

Backend вызывает его, когда при создании игрока нужно завести учётную запись
или при смене никнейма — переименовать её.
"""

import json
import urllib.error
import urllib.request

from django.conf import settings


class AuthServiceError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status  # HTTP-код ответа; None — сервис недоступен


def _call(method: str, path: str, payload: dict) -> dict:
    url = settings.AUTH_SERVICE_URL.rstrip("/") + path
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        method=method,
        headers={
            "Content-Type": "application/json",
            "X-Service-Token": settings.SERVICE_TOKEN,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read()).get("detail", str(e))
        except ValueError:
            detail = str(e)
        raise AuthServiceError(detail, status=e.code)
    except (urllib.error.URLError, TimeoutError):
        raise AuthServiceError("Сервис авторизации недоступен")


def create_user(username: str, password: str) -> int:
    return _call("POST", "/internal/users/", {"username": username, "password": password})["id"]


def rename_user(user_id: int, username: str) -> None:
    _call("PATCH", f"/internal/users/{user_id}/", {"username": username})
