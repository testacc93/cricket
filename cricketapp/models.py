from django.db import models
from django.db.models.aggregates import Count
import datetime
from smart_selects.db_fields import GroupedForeignKey

class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
         verbose_name_plural = "countries"


class Team(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    formed_date = datetime.datetime.now()
    score = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class Player(models.Model):

    name = models.CharField(max_length=256)
    country = models.ForeignKey(Country, max_length=256, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, max_length=256, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=25)
    total_runs = models.PositiveIntegerField(default=0)
    total_wickets = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Venue(models.Model):

    place = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.place


class Match(models.Model):

    winner_score = models.IntegerField(default=100)
    loser_score = models.IntegerField(default=100)
    winner_wickets = models.IntegerField(default=0)
    loser_wickets = models.IntegerField(default=0)
    name = models.CharField(max_length=256)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.DO_NOTHING)
    loser = models.ForeignKey(Team,related_name='loser', on_delete=models.DO_NOTHING, default=1)
    player_of_match = GroupedForeignKey(Player, 'team', related_name='player', default=1)
    bowler_of_match = GroupedForeignKey(Player, 'team', related_name='bowler', default=1)
    fielder_of_match = GroupedForeignKey(Player, 'team', related_name='fielder', default=1)

    def __str__(self):
        return self.name

    class Meta:
         verbose_name_plural = "Matches"


    # def get
    
    
