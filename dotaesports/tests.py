from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from dotaesports.models import *


# Create your tests here.
class TournamentsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_tournaments(self):
        tournament = Tournament.objects.create(
            name="БумБет Дача",
            start_date="2024-10-01",
            end_date="2024-10-02",
            status="Coming",
            prize_pool=500000
        )

        r = self.client.get('/api/tournaments/')
        data = r.json()
        
        assert tournament.name == data[0]['name']
        assert tournament.start_date == data[0]['start_date']
        assert tournament.end_date == data[0]['end_date']
        assert tournament.status == data[0]['status']
        assert tournament.prize_pool == data[0]['prize_pool']
        assert tournament.id == data[0]['id']

    def test_create_tournaments(self):
        # fields = ['id', 'name', 'start_date', 'end_date', 'status', 'prize_pool']
        tournament = baker.make("Tournament")

        r = self.client.get("/api/tournaments/")
        data = r.json()
        print(data)

        assert tournament.name == data[0]['name']
        assert tournament.start_date.isoformat() == data[0]['start_date']
        assert tournament.end_date.isoformat() == data[0]['end_date']
        assert tournament.status == data[0]['status']
        assert tournament.prize_pool == data[0]['prize_pool']

    def test_delete_tournaments(self):
        tournaments = baker.make("Tournament", 10)
        r = self.client.get('/api/tournaments/')
        data = r.json()
        
        assert len(data) == 10

        tournament_id_to_delete = tournaments[3].id

        self.client.delete(f'/api/tournaments/{tournament_id_to_delete}/')

        r = self.client.get('/api/tournaments/')
        data = r.json()
        
        assert len(data) == 9

        assert tournament_id_to_delete not in [i['id'] for i in data]

    def test_update_tournaments(self):
        tournaments = baker.make("Tournament", 10)
        tournament: Tournament = tournaments[2]

        r = self.client.get(f'/api/tournaments/{tournament.id}/')
        data = r.json()
        
        assert data['name'] == tournament.name

        r = self.client.put(f'/api/tournaments/{tournament.id}/',
        {
            'name': 'Зе Интернациональ',
            'start_date': tournament.start_date,
            'end_date': tournament.end_date,
            'prize_pool': tournament.prize_pool
        })
        
        print(r.json())
        assert r.status_code == 200

        r = self.client.get(f'/api/tournaments/{tournament.id}/')
        data = r.json()
        assert data['name'] == "Зе Интернациональ"

        tournament.refresh_from_db()
        assert data['name'] == tournament.name

class TeamsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_teams(self):
        team = Team.objects.create(
            name="Фиксики",
            country="Бангладеш"
        )

        r = self.client.get('/api/teams/')
        data = r.json()
        
        assert team.name == data[0]['name']
        assert team.country == data[0]['country']
        assert team.id == data[0]['id']

    def test_create_teams(self):
        team = baker.make("Team")

        r = self.client.get("/api/teams/")
        data = r.json()
        print(data)

        assert team.name == data[0]['name']
        assert team.country == data[0]['country']

    def test_delete_teams(self):
        teams = baker.make("Team", 10)
        r = self.client.get('/api/teams/')
        data = r.json()
        
        assert len(data) == 10

        team_id_to_delete = teams[3].id

        self.client.delete(f'/api/teams/{team_id_to_delete}/')

        r = self.client.get('/api/teams/')
        data = r.json()
        
        assert len(data) == 9

        assert team_id_to_delete not in [i['id'] for i in data]

    def test_update_teams(self):
        teams = baker.make("Team", 10)
        team: Team = teams[2]

        r = self.client.get(f'/api/teams/{team.id}/')
        data = r.json()
        
        assert data['name'] == team.name

        r = self.client.put(f'/api/teams/{team.id}/',
        {
            'name': 'Апокалипсис',
            'country': team.country
        })
        
        print(r.json())
        assert r.status_code == 200

        r = self.client.get(f'/api/teams/{team.id}/')
        data = r.json()
        assert data['name'] == "Апокалипсис"

        team.refresh_from_db()
        assert data['name'] == team.name

class PlayersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_players(self):
        # ['nickname', 'real_name', 'role', 'team']
        player_team = Team.objects.create(
            name="Карапузы",
            country="Китай"
        )
        player = Player.objects.create(
            nickname="iseedeadpeople",
            real_name="Фирамиров Геннадий",
            role="Керри",
            team=player_team
        )

        r = self.client.get('/api/players/')
        data = r.json()
        
        assert player.nickname == data[0]['nickname']
        assert player.real_name == data[0]['real_name']
        assert player.role == data[0]['role']
        assert player.id == data[0]['id']

    def test_create_players(self):
        player = baker.make("Player")

        r = self.client.get("/api/players/")
        data = r.json()
        print(data)

        assert player.nickname == data[0]['nickname']
        assert player.real_name == data[0]['real_name']
        assert player.role == data[0]['role']
        assert player.id == data[0]['id']

    def test_delete_players(self):
        players = baker.make("Player", 10)
        r = self.client.get('/api/players/')
        data = r.json()
        
        assert len(data) == 10

        player_id_to_delete = players[3].id

        self.client.delete(f'/api/players/{player_id_to_delete}/')

        r = self.client.get('/api/players/')
        data = r.json()
        
        assert len(data) == 9

        assert player_id_to_delete not in [i['id'] for i in data]

    def test_update_players(self):
        players = baker.make("Player", 10)
        player: Player = players[2]

        r = self.client.get(f'/api/players/{player.id}/')
        data = r.json()
        
        assert data['nickname'] == player.nickname

        r = self.client.put(f'/api/players/{player.id}/',
        {
            'nickname': 'chinchoppa',
            'real_name': player.real_name,
            'role': player.role,
        })
        
        print(r.json())
        assert r.status_code == 200

        r = self.client.get(f'/api/players/{player.id}/')
        data = r.json()
        assert data['nickname'] == "chinchoppa"

        player.refresh_from_db()
        assert data['nickname'] == player.nickname

class TournamentTeamParticipationsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_tournamentteamparticipations(self):
        ttp_tournament = Tournament.objects.create(
            name="CyberPolytech",
            start_date="2024-10-01",
            end_date="2024-10-02",
            status="Coming",
            prize_pool=500000
        )
        ttp_team = Team.objects.create(
            name="Шиншиллы",
            country="Ямайка"
        )
        ttp = TournamentTeamParticipation.objects.create(
            tournament=ttp_tournament,
            team=ttp_team,
            place=1
        )

        r = self.client.get('/api/tournamentsteamsparticipations/')
        data = r.json()
        
        assert ttp.tournament.id == data[0]['tournament']['id']
        assert ttp.team.id == data[0]['team']['id']
        assert ttp.id == data[0]['id']

    def test_create_tournamentteamparticipations(self):
        ttp_tournament = baker.make('Tournament')
        ttp_team = baker.make('Team')

        ttp = baker.make("TournamentTeamParticipation", tournament=ttp_tournament, team=ttp_team) 

        r = self.client.get("/api/tournamentsteamsparticipations/")
        data = r.json()
        print(data)

        assert ttp.tournament.id == data[0]['tournament']['id']
        assert ttp.team.id == data[0]['team']['id']
        assert ttp.id == data[0]['id']

    def test_delete_tournamentteamparticipations(self):
        ttps = baker.make("TournamentTeamParticipation", 10)
        r = self.client.get('/api/tournamentsteamsparticipations/')
        data = r.json()
        
        assert len(data) == 10

        ttp_id_to_delete = ttps[3].id

        self.client.delete(f'/api/tournamentsteamsparticipations/{ttp_id_to_delete}/')

        r = self.client.get('/api/tournamentsteamsparticipations/')
        data = r.json()
        
        assert len(data) == 9

        assert ttp_id_to_delete not in [i['id'] for i in data]

    def test_update_tournamentteamparticipations(self):
        ttps = baker.make("TournamentTeamParticipation", 10)
        ttp: TournamentTeamParticipation = ttps[2]

        r = self.client.get(f'/api/tournamentsteamsparticipations/{ttp.id}/')
        data = r.json()
        
        assert data['place'] == ttp.place

        r = self.client.put(f'/api/tournamentsteamsparticipations/{ttp.id}/',
        {
            'place': 32
        })
        
        print(r.json())
        assert r.status_code == 200

        r = self.client.get(f'/api/tournamentsteamsparticipations/{ttp.id}/')
        data = r.json()
        assert data['place'] == 32

        ttp.refresh_from_db()
        assert data['place'] == ttp.place

class MatchesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_matches(self):
        radiant_team = Team.objects.create(
            name="Тестики вторые",
            country="Гренландия"
        )
        dire_team = Team.objects.create(
            name="Тестики первые",
            country="Перу"
        )
        match_tournament = Tournament.objects.create(
            name="Обеликс",
            start_date="2024-10-01",
            end_date="2024-10-02",
            status="Coming",
            prize_pool=1500000
        )
        match = Match.objects.create(
            tournament=match_tournament,
            radiant=radiant_team,
            dire=dire_team,
            start_date="2024-10-05T00:00:00.000000",
            winner=radiant_team
        )

        r = self.client.get('/api/matches/')
        data = r.json()
        
        assert match.tournament.id == data[0]['tournament']['id']
        assert match.radiant.id == data[0]['radiant']['id']
        assert match.dire.id == data[0]['dire']['id']
        assert match.start_date == data[0]['start_date']
        assert match.winner.id == data[0]['winner']['id']


    def test_create_matches(self):
        radiant_team = baker.make('Team')
        dire_team = baker.make('Team')
        match_tournament = baker.make('Tournament')

        match = baker.make("Match", radiant=radiant_team, dire=dire_team, tournament=match_tournament) 

        r = self.client.get("/api/matches/")
        data = r.json()
        print(data)

        assert match.tournament.id == data[0]['tournament']['id']
        assert match.radiant.id == data[0]['radiant']['id']
        assert match.dire.id == data[0]['dire']['id']
        assert match.start_date.isoformat().replace('+00:00', 'Z') == data[0]['start_date']
        assert match.winner == data[0]['winner']

    def test_delete_matches(self):
        matches = baker.make("Match", 10)
        r = self.client.get('/api/matches/')
        data = r.json()
        
        assert len(data) == 10

        match_id_to_delete = matches[3].id

        self.client.delete(f'/api/matches/{match_id_to_delete}/')

        r = self.client.get('/api/matches/')
        data = r.json()
        
        assert len(data) == 9

        assert match_id_to_delete not in [i['id'] for i in data]

    def test_update_matches(self):
        matches = baker.make("Match", 10)
        match: Match = matches[2]

        r = self.client.get(f'/api/matches/{match.id}/')
        data = r.json()
        
        assert data['start_date'] == match.start_date.isoformat()

        r = self.client.put(f'/api/matches/{match.id}/',
        {
            'start_date': "2024-10-21T12:42:07.057511", 
        })
        
        print(r.json())
        assert r.status_code == 200

        r = self.client.get(f'/api/matches/{match.id}/')
        data = r.json()
        assert data['start_date'] == "2024-10-21T12:42:07.057511"

        match.refresh_from_db()
        assert data['start_date'] == match.start_date.isoformat()