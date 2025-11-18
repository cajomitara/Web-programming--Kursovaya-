from rest_framework import serializers

from django.contrib.auth.models import User 
from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'status', 'prize_pool', 'logo']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country', 'logo']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='team', 
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )

    class Meta:
        model = Player
        fields = ['id', 'user', 'user_id', 'nickname', 'real_name', 'role', 'team', 'team_id', 'photo']

class TournamentTeamParticipationSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    tournament_id = serializers.PrimaryKeyRelatedField(
        queryset=Tournament.objects.all(), 
        source='tournament', 
        write_only=True
    )
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='team', 
        write_only=True
    )

    class Meta:
        model = TournamentTeamParticipation
        fields = ['id', 'tournament', 'tournament_id', 'team', 'team_id', 'place']

class MatchSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    radiant = TeamSerializer(read_only=True)
    dire = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)

    tournament_id = serializers.PrimaryKeyRelatedField(
        queryset=Tournament.objects.all(), 
        source='tournament', 
        write_only=True
    )
    radiant_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='radiant', 
        write_only=True
    )
    dire_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='dire', 
        write_only=True
    )
    winner_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='winner', 
        write_only=True,
        allow_null=True
    )

    start_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')
    
    class Meta:
        model = Match
        fields = ['id', 'tournament', 'tournament_id', 'radiant', 'radiant_id', 'dire', 'dire_id', 'start_date', 'winner', 'winner_id']
