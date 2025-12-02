from django.core.management.base import BaseCommand

from faker import Faker

from dotaesports.models import Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(10):
            Team.objects.create(
                name=fake.name()
            )