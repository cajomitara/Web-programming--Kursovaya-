import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from dotaesports.models import (
    Tournament, Team, Player, 
    TournamentTeamParticipation, Match
)
from dotaesports.serializers import PlayerSerializer
from django.test import RequestFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        Tournament.objects.all().delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        TournamentTeamParticipation.objects.all().delete()
        Match.objects.all().delete()

        try:
            manager_user = User.objects.create_user(
                username='script_manager',
                password='dotaesports'
            )
        except:
            manager_user = User.objects.get(username='script_manager')

        self.generate_tournaments(fake, count=20)
        self.generate_teams(fake, count=20)
        self.generate_players(fake, count=100, manager_user=manager_user)
        self.generate_team_participations(fake)
        self.generate_matches(fake)
    
    def generate_tournaments(self, fake, count):
        for i in range(count):
            start_date = fake.date_between(start_date='-2y', end_date='+1y')
            
            duration = random.randint(1, 30)
            end_date = start_date + timedelta(days=duration)
            
            now = datetime.now().date()
            if end_date < now:
                status = 'Ended'
            elif start_date > now:
                status = random.choice(['TBA', 'Coming'])
            else:
                status = 'Live'
            
            Tournament.objects.create(
                name=f"Турнир {fake.word().capitalize()} {fake.city()} {i+1}",
                start_date=start_date,
                end_date=end_date,
                status=status,
                prize_pool=random.randint(10000, 10000000)
            )
    
    def generate_teams(self, fake, count):     
        countries = ['Россия', 'Беларусь', 'Казахстан', 'США', 'Китай', 'Германия', 'Корея', 'Япония', 'Бразилия']
        
        team_prefixes = ['Team', 'Esports', 'Gaming', 'Pro', 'Elite', 'Cyber', 'Digital', 'Victory', 'Legacy', 'Nova']
        team_suffixes = ['Gaming', 'Esports', 'Team', 'Pro', 'Legends', 'Warriors', 'Kings', 'Dragons', 'Phoenix', 'Titans']
        
        for i in range(count):
            name = f"{random.choice(team_prefixes)} {fake.word().capitalize()} {random.choice(team_suffixes)}"
            
            Team.objects.create(
                name=name,
                country=random.choice(countries)
            )
    
    def generate_players(self, fake, count, manager_user):
        teams = list(Team.objects.all())
        if not teams:
            return
        
        roles = [choice[0] for choice in Player.Role.choices]
        
        for _ in range(count):
            first_name = fake.first_name_male() if random.choice([True, False]) else fake.first_name_female()
            last_name = fake.last_name_male() if random.choice([True, False]) else fake.last_name_female()

            nickname_options = [
                f"{first_name}_{random.randint(1, 999)}",
                f"{fake.word().capitalize()}{random.randint(1, 999)}",
                f"{last_name}{random.randint(1, 99)}",
                f"{fake.word()}_{fake.word()}"
            ]
            nickname = random.choice(nickname_options)

            team = random.choice(teams)

            factory = RequestFactory()
            request = factory.get('/')
            request.user = manager_user 

            player_data = {
                "nickname": nickname,
                "real_name": f"{first_name} {last_name}",
                "role": random.choice(roles),
                "team_id": team.id
            }

            serializer = PlayerSerializer(data=player_data)
            serializer.is_valid()
            serializer.save()

    
    def generate_team_participations(self, fake):
        tournaments = list(Tournament.objects.all())
        teams = list(Team.objects.all())
        
        if not tournaments or not teams:
            return
        
        for tournament in tournaments:
            num_teams = random.randint(8, 32)
            selected_teams = random.sample(teams, min(num_teams, len(teams)))

            places = list(range(1, len(selected_teams) + 1))
            random.shuffle(places)
            
            for i, team in enumerate(selected_teams):
                TournamentTeamParticipation.objects.create(
                    tournament=tournament,
                    team=team,
                    place=places[i]
                )
    
    def generate_matches(self, fake):
        tournaments = list(Tournament.objects.all())
        
        for tournament in tournaments:
            participations = TournamentTeamParticipation.objects.filter(tournament=tournament)
            tournament_teams = [p.team for p in participations]
            
            if len(tournament_teams) < 2:
                continue
            
            num_matches = random.randint(10, 50)

            start_date = tournament.start_date
            end_date = tournament.end_date
            
            if start_date and end_date:
                for _ in range(num_matches):
                    days_between = (end_date - start_date).days
                    if days_between > 0:
                        random_days = random.randint(0, days_between)
                        match_date = start_date + timedelta(days=random_days)
                        
                        match_datetime = datetime.combine(
                            match_date,
                            datetime.min.time()
                        ) + timedelta(hours=random.randint(10, 22))
                        
                        if len(tournament_teams) >= 2:
                            radiant, dire = random.sample(tournament_teams, 2)
                            
                            winner = random.choice([radiant, dire])
                            
                            Match.objects.create(
                                tournament=tournament,
                                radiant=radiant,
                                dire=dire,
                                start_date=match_datetime,
                                winner=winner
                            )