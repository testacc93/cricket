from django.db.models import fields
from rest_framework import serializers
from cricketapp.models import Country, Match, Player, Team, Venue
from django.utils import tree

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name','country', 'formed_date', 'score']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(rep)
        rep['country'] = CountrySerializer(instance.country).data['name']
        return rep


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name','country', 'age', 'total_runs', 'total_wickets']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['country'] = CountrySerializer(instance.country).data['name']
        return rep


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['place','country']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['country'] = CountrySerializer(instance.country).data['name']
        return rep


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['name','winner','loser','winner_score','loser_score', 'winner_wickets', 'loser_wickets',  'player_of_match', 'bowler_of_match', 'fielder_of_match']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['winner'] = CountrySerializer(instance.winner).data['name']
        rep['loser'] = CountrySerializer(instance.loser).data['name']
        rep['player_of_match'] = PlayerSerializer(instance.player_of_match).data['name']
        rep['bowler_of_match'] = PlayerSerializer(instance.bowler_of_match).data['name']
        rep['fielder_of_match'] = PlayerSerializer(instance.fielder_of_match).data['name']
        return rep


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name','score']


        