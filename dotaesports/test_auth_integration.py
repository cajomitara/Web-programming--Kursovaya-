"""
Тесты взаимодействия backend с сервисом авторизации:
- проверка JWT из cookie (без обращения к сервису авторизации);
- вызовы внутреннего API при создании и переименовании игрока (сервис подменяется mock-объектом).
"""

import time
from unittest import mock

import jwt
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from dotaesports import auth_client
from dotaesports.models import Player, PlayerTeamHistory, Team


def make_token(user_id, username, is_staff=False, secret=None, exp_offset=3600):
    now = int(time.time())
    return jwt.encode(
        {"sub": str(user_id), "username": username, "is_staff": is_staff,
         "iat": now, "exp": now + exp_offset},
        secret or settings.JWT_SECRET,
        algorithm="HS256",
    )


class JWTAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_a = Team.objects.create(name="Team A", country="Россия")
        self.team_b = Team.objects.create(name="Team B", country="Китай")
        Player.objects.create(nickname="player_a", team=self.team_a, auth_user_id=42)

    def test_player_sees_only_own_team(self):
        self.client.cookies[settings.JWT_COOKIE_NAME] = make_token(42, "player_a")
        data = self.client.get('/api/teams/').json()
        assert [t['name'] for t in data] == ["Team A"]

    def test_staff_sees_all_teams(self):
        self.client.cookies[settings.JWT_COOKIE_NAME] = make_token(1, "admin", is_staff=True)
        data = self.client.get('/api/teams/').json()
        assert len(data) == 2

    def test_forged_token_is_anonymous(self):
        self.client.cookies[settings.JWT_COOKIE_NAME] = make_token(42, "player_a", secret="wrong-secret")
        r = self.client.get('/api/teams/')
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_expired_token_is_anonymous(self):
        self.client.cookies[settings.JWT_COOKIE_NAME] = make_token(42, "player_a", exp_offset=-10)
        assert len(self.client.get('/api/teams/').json()) == 2


class AuthServiceCallsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.cookies[settings.JWT_COOKIE_NAME] = make_token(7, "manager", is_staff=True)
        self.team = Team.objects.create(name="Team A", country="Россия")

    @mock.patch("dotaesports.auth_client.create_user", return_value=777)
    def test_create_player_creates_account(self, create_user):
        r = self.client.post('/api/players/', {'nickname': 'yatoro', 'role': 'CARRY', 'team_id': self.team.id})
        assert r.status_code == 201

        create_user.assert_called_once_with(username='yatoro', password='dotaesports')
        player = Player.objects.get(nickname='yatoro')
        assert player.auth_user_id == 777

        history = PlayerTeamHistory.objects.get(player=player)
        assert history.manager_user_id == 7
        assert history.manager_username == "manager"

    @mock.patch("dotaesports.auth_client.create_user",
                side_effect=auth_client.AuthServiceError("exists", status=409))
    def test_create_player_with_taken_username(self, create_user):
        r = self.client.post('/api/players/', {'nickname': 'yatoro', 'role': 'CARRY'})
        assert r.status_code == 400
        assert not Player.objects.filter(nickname='yatoro').exists()

    @mock.patch("dotaesports.auth_client.create_user",
                side_effect=auth_client.AuthServiceError("Сервис авторизации недоступен"))
    def test_create_player_when_auth_service_down(self, create_user):
        r = self.client.post('/api/players/', {'nickname': 'yatoro', 'role': 'CARRY'})
        assert r.status_code == 503
        assert not Player.objects.filter(nickname='yatoro').exists()

    @mock.patch("dotaesports.auth_client.rename_user")
    def test_rename_player_renames_account(self, rename_user):
        player = Player.objects.create(nickname='old_nick', role='CARRY', auth_user_id=55)
        r = self.client.patch(f'/api/players/{player.id}/', {'nickname': 'new_nick'})
        assert r.status_code == 200
        rename_user.assert_called_once_with(55, 'new_nick')
