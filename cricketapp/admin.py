from django.contrib import admin

from cricketapp.models import Country, Match, Player, Team, Venue

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Country, CountryAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']

admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'country', 'team', 'total_runs', 'total_wickets']

admin.site.register(Player, PlayerAdmin)


class VenueAdmin(admin.ModelAdmin):
    list_display = ['id','place', 'country']

admin.site.register(Venue, VenueAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'player_of_match', 'winner', 'loser']
    exclude = ['name']

admin.site.register(Match, MatchAdmin)