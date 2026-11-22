import json

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="miracle", password="secret-pass-123")

    def login(self, password="secret-pass-123"):
        return self.client.post(
            "/api/users/login/",
            json.dumps({"username": "miracle", "password": password}),
            content_type="application/json",
        )

    def test_login_success_sets_jwt_cookie(self):
        r = self.login()
        assert r.status_code == 200
        token = r.cookies[settings.JWT_COOKIE_NAME].value
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        assert payload["sub"] == str(self.user.id)
        assert payload["username"] == "miracle"
        assert r.cookies[settings.JWT_COOKIE_NAME]["httponly"]

    def test_login_wrong_password(self):
        r = self.login(password="wrong")
        assert r.status_code == 401
        assert settings.JWT_COOKIE_NAME not in r.cookies

    def test_my_anonymous(self):
        r = self.client.get("/api/users/my/")
        assert r.json()["is_authenticated"] is False

    def test_my_after_login(self):
        self.login()
        r = self.client.get("/api/users/my/")
        data = r.json()
        assert data["is_authenticated"] is True
        assert data["username"] == "miracle"
        assert data["is_staff"] is False

    def test_my_with_forged_token(self):
        forged = jwt.encode({"sub": str(self.user.id), "username": "miracle", "is_staff": True},
                            "not-the-real-secret", algorithm="HS256")
        self.client.cookies[settings.JWT_COOKIE_NAME] = forged
        r = self.client.get("/api/users/my/")
        assert r.json()["is_authenticated"] is False

    def test_logout_deletes_cookie(self):
        self.login()
        r = self.client.post("/api/users/logout/")
        assert r.status_code == 200
        assert r.cookies[settings.JWT_COOKIE_NAME].value == ""


class InternalApiTestCase(TestCase):
    def headers(self, token=None):
        return {"HTTP_X_SERVICE_TOKEN": token if token is not None else settings.SERVICE_TOKEN}

    def test_create_requires_service_token(self):
        r = self.client.post("/internal/users/", json.dumps({"username": "ana", "password": "p"}),
                             content_type="application/json", **self.headers("bad"))
        assert r.status_code == 403
        assert not User.objects.filter(username="ana").exists()

    def test_create_user_and_conflict(self):
        r = self.client.post("/internal/users/", json.dumps({"username": "ana", "password": "dotaesports"}),
                             content_type="application/json", **self.headers())
        assert r.status_code == 201
        user = User.objects.get(username="ana")
        assert r.json()["id"] == user.id
        assert user.check_password("dotaesports")

        r = self.client.post("/internal/users/", json.dumps({"username": "ana", "password": "x"}),
                             content_type="application/json", **self.headers())
        assert r.status_code == 409

    def test_rename_user(self):
        user = User.objects.create_user(username="old_name", password="p")
        User.objects.create_user(username="taken", password="p")

        r = self.client.patch(f"/internal/users/{user.id}/", json.dumps({"username": "taken"}),
                              content_type="application/json", **self.headers())
        assert r.status_code == 409

        r = self.client.patch(f"/internal/users/{user.id}/", json.dumps({"username": "new_name"}),
                              content_type="application/json", **self.headers())
        assert r.status_code == 200
        user.refresh_from_db()
        assert user.username == "new_name"


class HealthTestCase(TestCase):
    def test_health(self):
        assert self.client.get("/health/live/").status_code == 200
        assert self.client.get("/health/ready/").status_code == 200
