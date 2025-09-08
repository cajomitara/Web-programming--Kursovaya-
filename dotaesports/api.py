from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from dotaesports.models import Tournament
from dotaesports.serializers import TournamentSerializer

class TournamentViewset(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
