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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from dotaesports import views
from dotaesports.api import TournamentViewset, TeamViewset, PlayerViewset, TournamentTeamParticipationViewset, MatchViewset, UserViewset


router = DefaultRouter()
router.register("tournaments", TournamentViewset, basename="tournaments")
router.register("teams", TeamViewset, basename="teams")
router.register("players", PlayerViewset, basename="players")
router.register("tournamentsteamsparticipations", TournamentTeamParticipationViewset, basename="tournamentsteamsparticipations")
router.register("matches", MatchViewset, basename="matches")
router.register("users", UserViewset, basename="users")

urlpatterns = [
    path('tournaments/', views.ShowTournamentsView.as_view()),
    path('teams/', views.ShowTeamsView.as_view()),
    path('players/', views.ShowPlayersView.as_view()),
    path('tournamentsteamsparticipations/', views.ShowTournamentTeamParticipationsView.as_view()),
    path('matches/', views.ShowMatchTeamParticipationsView.as_view()),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
