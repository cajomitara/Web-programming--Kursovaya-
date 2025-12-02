from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from django.contrib.auth.models import User
from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match, PlayerTeamHistory
from dotaesports.serializers import TournamentSerializer, TeamSerializer, PlayerSerializer, TournamentTeamParticipationSerializer, MatchSerializer, PlayerTeamHistorySerializer

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



    def get_queryset(self):
        qs = super().get_queryset()
        # if self.request.user.is_authenticated:
        #     qs = qs.filter(user=self.request.user)
        return qs

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

# class UserViewset(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class PlayerTeamHistoryViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = PlayerTeamHistory.objects.all()
    serializer_class = PlayerTeamHistorySerializer
    
    def get_queryset(self):
        qs = super().get_queryset()

        player_id = self.request.query_params.get('player_id')
        if player_id:
            qs = qs.filter(player_id=player_id)

        team_id = self.request.query_params.get('team_id')
        if team_id:
            qs = qs.filter(team_id=team_id)

        qs = qs.order_by('-created_at')
        
        return qs