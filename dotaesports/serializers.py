from rest_framework import serializers
from django.contrib.auth.models import User 
from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match, PlayerTeamHistory

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
    # создание пользователя при создании игрока
    def create(self, validated_data):
        nickname = validated_data.get('nickname')
        
        if Player.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError({"nickname": "Игрок с таким никнеймом уже существует"})
        
        username = nickname
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"nickname": "Пользователь с таким именем уже существует"})

        user = User.objects.create_user(
            username=username,
            password='dotaesports'
        )
        
        validated_data['user'] = user
        
        team = validated_data.get('team')

        player = super().create(validated_data)
        
        request = self.context.get('request')
        manager = request.user if request else None
            
        PlayerTeamHistory.objects.create(
            player=player,
            team=team,
            manager=manager
        )

        return player
    
    # изменение пользователя при изменении игрока
    def update(self, instance, validated_data):
        nickname = validated_data.get('nickname')

        if nickname and nickname != instance.nickname:
            if Player.objects.filter(nickname=nickname).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"nickname": "Игрок с таким никнеймом уже существует"})
            
            user = instance.user
            if user:
                if User.objects.filter(username=nickname).exclude(id=user.id).exists():
                    raise serializers.ValidationError({"nickname": "Пользователь с таким именем уже существует"})
                
                user.username = nickname
                user.save()
        
        old_team = instance.team
        new_team = validated_data.get('team', old_team)

        player = super().update(instance, validated_data)

        if new_team != old_team:
            request = self.context.get('request')
            manager = request.user
            
            PlayerTeamHistory.objects.create(
                player=player,
                team=new_team,
                manager=manager
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
    manager = UserSerializer(read_only=True)
    
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
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='manager',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = PlayerTeamHistory
        fields = ['id', 'player', 'player_id', 'team', 'team_id', 
                 'manager', 'manager_id', 'created_at']