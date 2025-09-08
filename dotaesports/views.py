from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match

# Create your views here.

class ShowTournamentsView(TemplateView):
    template_name = "tournaments/show_tournaments.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context['tournaments'] = Tournament.objects.all()
        
        return context