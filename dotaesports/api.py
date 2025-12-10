from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match, PlayerTeamHistory
from dotaesports.serializers import TournamentSerializer, TeamSerializer, PlayerSerializer, TournamentTeamParticipationSerializer, MatchSerializer, PlayerTeamHistorySerializer, UserSerializer

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

class UserViewset(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, *args, **kwargs):
        return Response({
            'username': self.request.user.username,
            'is_authenticated': self.request.user.is_authenticated,
            'is_staff': self.request.user.is_staff
        })
    
    @action(url_path="login", methods=["POST"], detail=False)
    def process_login(self, *args, **kwargs):
        class LoginSerializer(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()

        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            login(request=self.request, user=user)
        else:
            return Response({
                "status": "Failed!"
            }, status=401)
        return Response({
                "status": "Success!"
        })
    
    @action(url_path="logout", methods=["POST"], detail=False)
    def process_logout(self, *args, **kwargs):
        logout(self.request)

        return Response({
                "status": "Success!"
        })

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