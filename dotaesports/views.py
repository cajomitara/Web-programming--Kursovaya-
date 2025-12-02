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
        context['objects'] = Tournament.objects.all()
        
        return context
    
class ShowTeamsView(TemplateView):
    template_name = "teams/show_teams.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context['objects'] = Team.objects.all()
        
        return context
    
class ShowPlayersView(TemplateView):
    template_name = "players/show_players.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context['objects'] = Player.objects.all()
        
        return context
    


class ShowTournamentTeamParticipationsView(TemplateView):
    template_name = "teamparticipations/show_teamparticipations.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context['objects'] = TournamentTeamParticipation.objects.all()
        
        return context
    
class ShowMatchTeamParticipationsView(TemplateView):
    template_name = "matches/show_matches.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context['objects'] = Match.objects.all()
        
        return context