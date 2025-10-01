from django.test import TestCase
from django import APIClient

# Create your tests here.
class TournamentViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/students/')
        print(r)