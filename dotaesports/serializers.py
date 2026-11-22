from rest_framework import serializers
from rest_framework.exceptions import APIException
from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match, PlayerTeamHistory
from dotaesports import auth_client


class AuthServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Сервис авторизации недоступен"


def _raise_for_auth_error(error):
    # 409 — имя занято (ошибка валидации), остальное — проблема на стороне сервиса
    if error.status == 409:
        raise serializers.ValidationError({"nickname": "Пользователь с таким именем уже существует"})
    raise AuthServiceUnavailable(str(error))


def _current_manager(context):
    # пользователь берётся из JWT (dotaesports.authentication.TokenUser)
    request = context.get('request')
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return user.id, user.username
    return None, None

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'status', 'prize_pool', 'logo']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country', 'logo']

class PlayerSerializer(serializers.ModelSerializer):
    # создание учётной записи в сервисе авторизации при создании игрока
    def create(self, validated_data):
        nickname = validated_data.get('nickname')
        
        if Player.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError({"nickname": "Игрок с таким никнеймом уже существует"})

        try:
            validated_data['auth_user_id'] = auth_client.create_user(username=nickname, password='dotaesports')
        except auth_client.AuthServiceError as error:
            _raise_for_auth_error(error)
        
        team = validated_data.get('team')

        player = super().create(validated_data)
        
        manager_id, manager_username = _current_manager(self.context)
        PlayerTeamHistory.objects.create(
            player=player,
            team=team,
            manager_user_id=manager_id,
            manager_username=manager_username
        )

        return player
    
    # переименование учётной записи при изменении никнейма игрока
    def update(self, instance, validated_data):
        nickname = validated_data.get('nickname')

        if nickname and nickname != instance.nickname:
            if Player.objects.filter(nickname=nickname).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"nickname": "Игрок с таким никнеймом уже существует"})
            
            if instance.auth_user_id:
                try:
                    auth_client.rename_user(instance.auth_user_id, nickname)
                except auth_client.AuthServiceError as error:
                    _raise_for_auth_error(error)
        
        old_team = instance.team
        new_team = validated_data.get('team', old_team)

        player = super().update(instance, validated_data)

        if new_team != old_team:
            manager_id, manager_username = _current_manager(self.context)
            PlayerTeamHistory.objects.create(
                player=player,
                team=new_team,
                manager_user_id=manager_id,
                manager_username=manager_username
            )
        return player
    
    
    team = TeamSerializer(read_only=True)
    
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='team', 
        write_only=True,
        required=False,
        allow_null=True
    )

    # team_history = serializers.SerializerMethodField(read_only=True)
    
    # def get_team_history(self, obj):
    #     history = obj.team_history.all()[:10]
    #     return PlayerTeamHistorySerializer(history, many=True, context=self.context).data
    
    class Meta:
        model = Player
        fields = ['id', 'nickname', 'real_name', 'role', 'team', 'team_id', 'photo']

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

    class Meta:
        model = Match
        fields = ['id', 'tournament', 'tournament_id', 'radiant', 'radiant_id', 
                  'dire', 'dire_id', 'start_date', 'winner', 'winner_id']
        
class PlayerTeamHistorySerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    manager = serializers.CharField(source='manager_username', read_only=True)
    
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(),
        source='player',
        write_only=True,
        required=False
    )
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True,
        required=False,
        allow_null=True
    )
    manager_user_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = PlayerTeamHistory
        fields = ['id', 'player', 'player_id', 'team', 'team_id', 
                 'manager', 'manager_user_id', 'created_at']