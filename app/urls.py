"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path, re_path
from django.http import JsonResponse
from django.db import connection
from django.views.static import serve
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import JsonResponse
from django.db import connection
from django.views.static import serve

from rest_framework.routers import DefaultRouter

from dotaesports import views
from dotaesports.api import TournamentViewset, TeamViewset, PlayerViewset, TournamentTeamParticipationViewset, MatchViewset, PlayerTeamHistoryViewset


def health_live(request):
    # «процесс жив»: без обращения к БД
    return JsonResponse({"status": "ok"})


def health_ready(request):
    # «готов принимать трафик»: БД доступна
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "db unavailable"}, status=503)
    return JsonResponse({"status": "ok"})


router = DefaultRouter()
router.register("tournaments", TournamentViewset, basename="tournaments")
router.register("teams", TeamViewset, basename="teams")
router.register("players", PlayerViewset, basename="players")
router.register("tournamentsteamsparticipations", TournamentTeamParticipationViewset, basename="tournamentsteamsparticipations")
router.register("matches", MatchViewset, basename="matches")
router.register('player-team-history', PlayerTeamHistoryViewset, basename="playerteamhistory")

urlpatterns = [
    path('api/health/live/', health_live),
    path('api/health/ready/', health_ready),

    path('tournaments/', views.ShowTournamentsView.as_view()),
    path('teams/', views.ShowTeamsView.as_view()),
    path('players/', views.ShowPlayersView.as_view()),
    path('tournamentsteamsparticipations/', views.ShowTournamentTeamParticipationsView.as_view()),
    path('matches/', views.ShowMatchTeamParticipationsView.as_view()),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
