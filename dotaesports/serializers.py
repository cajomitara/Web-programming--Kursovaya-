from rest_framework import serializers

from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'status', 'prize_pool']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'nickname', 'real_name', 'role', 'team']

class TournamentTeamParticipationSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TournamentTeamParticipation
        fields = ['id', 'tournament', 'team', 'place']

class MatchSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    radiant = TeamSerializer(read_only=True)
    dire = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'tournament', 'radiant', 'dire', 'start_date', 'winner']
