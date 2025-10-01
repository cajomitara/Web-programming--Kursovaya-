from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from dotaesports.models import *

# Create your tests here.
class TournamentViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_tournament(self):
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

    def test_create_tournament(self):
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

    def test_delete_tournament(self):
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

    def test_update_tournament(self):
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

