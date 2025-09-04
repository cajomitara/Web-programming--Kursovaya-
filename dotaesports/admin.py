from django.contrib import admin

from dotaesports.models import Tournament, Team, Player, TournamentTeamParticipation, Match


# Register your models here.
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'status', 'prize_pool']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'real_name', 'role', 'team']

@admin.register(TournamentTeamParticipation)
class TournamentTeamParticipationAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'team', 'place']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'radiant', 'dire', 'start_date', 'winner']