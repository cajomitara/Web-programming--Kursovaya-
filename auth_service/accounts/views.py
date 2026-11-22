"""
API сервиса авторизации.

Публичная часть (доступна через шлюз nginx по /api/users/):
    POST /api/users/login/   — вход, выдаёт JWT в HttpOnly-cookie access_token
    POST /api/users/logout/  — выход, удаляет cookie
    GET  /api/users/my/      — информация о текущем пользователе

Внутренняя часть (шлюз её НЕ публикует, вызывается только другими сервисами
с заголовком X-Service-Token):
    POST  /internal/users/            — создать пользователя
    PATCH /internal/users/<id>/       — переименовать пользователя
"""

import hmac
import json

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from accounts.tokens import decode_token, issue_token

ANONYMOUS = {"id": None, "username": "", "is_authenticated": False, "is_staff": False}


def _read_json(request) -> dict:
    try:
        data = json.loads(request.body or b"{}")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def _is_trusted_service(request) -> bool:
    token = request.headers.get("X-Service-Token", "")
    return hmac.compare_digest(token, settings.SERVICE_TOKEN)


# ---------- публичный API ----------

@csrf_exempt
@require_POST
def login_view(request):
    data = _read_json(request)
    user = authenticate(request, username=data.get("username"), password=data.get("password"))
    if user is None or not user.is_active:
        return JsonResponse({"status": "Failed!"}, status=401)

    response = JsonResponse({"status": "Success!"})
    response.set_cookie(
        settings.JWT_COOKIE_NAME,
        issue_token(user),
        max_age=settings.JWT_LIFETIME_SECONDS,
        httponly=True,      # токен недоступен JavaScript
        samesite="Lax",     # cookie не отправляется с запросами с чужих сайтов
        path="/",
    )
    return response


@csrf_exempt
@require_POST
def logout_view(request):
    response = JsonResponse({"status": "Success!"})
    response.delete_cookie(settings.JWT_COOKIE_NAME, path="/", samesite="Lax")
    return response


@require_GET
def my_view(request):
    token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
    if not token:
        return JsonResponse(ANONYMOUS)
    try:
        payload = decode_token(token)
    except jwt.InvalidTokenError:
        return JsonResponse(ANONYMOUS)

    # сервис владеет учётными записями, поэтому отдаёт актуальные данные из своей БД
    user = User.objects.filter(id=int(payload["sub"]), is_active=True).first()
    if user is None:
        return JsonResponse(ANONYMOUS)
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "is_authenticated": True,
        "is_staff": user.is_staff,
    })


# ---------- внутренний API ----------

@csrf_exempt
@require_POST
def internal_create_user(request):
    if not _is_trusted_service(request):
        return JsonResponse({"detail": "Forbidden"}, status=403)

    data = _read_json(request)
    username = (data.get("username") or "").strip()
    if not username:
        return JsonResponse({"detail": "Не указано имя пользователя"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "Пользователь с таким именем уже существует"}, status=409)

    user = User.objects.create_user(username=username, password=data.get("password"))
    return JsonResponse({"id": user.id, "username": user.username}, status=201)


@csrf_exempt
@require_http_methods(["PATCH"])
def internal_update_user(request, user_id):
    if not _is_trusted_service(request):
        return JsonResponse({"detail": "Forbidden"}, status=403)

    user = User.objects.filter(id=user_id).first()
    if user is None:
        return JsonResponse({"detail": "Пользователь не найден"}, status=404)

    username = (_read_json(request).get("username") or "").strip()
    if not username:
        return JsonResponse({"detail": "Не указано имя пользователя"}, status=400)
    if User.objects.filter(username=username).exclude(id=user.id).exists():
        return JsonResponse({"detail": "Пользователь с таким именем уже существует"}, status=409)

    user.username = username
    user.save(update_fields=["username"])
    return JsonResponse({"id": user.id, "username": user.username})


# ---------- проверки состояния для Kubernetes ----------

def health_live(request):
    return JsonResponse({"status": "ok"})


def health_ready(request):
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "db unavailable"}, status=503)
    return JsonResponse({"status": "ok"})
