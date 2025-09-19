from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match
from dotaesports.serializers import TournamentSerializer, TeamSerializer, PlayerSerializer, TournamentTeamParticipationSerializer, MatchSerializer

class TournamentViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TeamViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class TournamentTeamParticipationViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TournamentTeamParticipation.objects.all()
    serializer_class = TournamentTeamParticipationSerializer

class MatchViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer