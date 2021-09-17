from django.core.checks.messages import Error
from django.shortcuts import render
from rest_framework.serializers import Serializer, SerializerMetaclass
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics,status, exceptions
from django.db.models import F

from cricketapp import serializers
from cricketapp import models
from cricketapp.mixins import get_country, get_player, get_team, get_venue
from cricketapp.models import Country, Team, Player
from cricketapp.serializers import CountrySerializer, TeamSerializer, PlayerSerializer,VenueSerializer, MatchSerializer, ScoreSerializer


class GetCountryAPIView(APIView):
    serlizer_class = CountrySerializer

    @swagger_auto_schema(tags=['Countries'], operation_description='Lists out all countries')
    def get(self, request,searchkey=''):
        if searchkey == "":
            countries_qs = models.Country.objects.all()
        else:
            countries_qs = models.Country.objects.filter(name__contains=searchkey)
        ser = self.serlizer_class(countries_qs, many=True)
        return Response({'Countries':ser.data})


class CreateCountryAPIView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    @swagger_auto_schema(tags=['Countries'], operation_description='Creates a country')
    def post(self, request):
        data = request.data
        name_country = (request.data['name']).lower()
        if len(name_country) < 1:
            return Response({'message':'country name can not be empty'})
        if models.Country.objects.filter(name=name_country).exists():
            return Response({'message':'Country already exists'})
        models.Country.objects.create(name=(data['name']).lower())
        return Response({'message':'success', 'data':request.data['name']})


class UpdateCountryAPIView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    @swagger_auto_schema(tags=['Countries'], operation_description='Alters the name of a country')
    def put(self, request, id):
        data = request.data
        country_change = get_country(id)
        country_new_name = request.data['name']
        if country_change is None:
            return Response({'message':'Country not found'}, status=status.HTTP_404_NOT_FOUND)
        if country_exist := models.Country.objects.get(name=data['name']):
            return Response({'message':'Country with same name exists'},status=status.HTTP_400_BAD_REQUEST)
        models.Country.objects.filter(id=id).update(name=country_new_name)
        return Response({'message':'Successfully changed country name'},status=status.HTTP_200_OK)


class DeleteCountryAPIView(generics.DestroyAPIView):
    serializer_class = CountrySerializer

    @swagger_auto_schema(tags=['Countries'], operation_description='deletes a country')
    def delete(self, request, id):
        try:
            models.Country.objects.get(id=id)
        except:
            return Response({'message':'Country with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Country.objects.filter(id=id).delete()
        return Response({'message':'success'})


class GetTeamAPIView(APIView):
    serlizer_class = TeamSerializer

    @swagger_auto_schema(tags=['Teams'], operation_description='List outs all the teams')
    def get(self, request):
        team_qs = models.Team.objects.all()
        ser = self.serlizer_class(team_qs, many=True)
        return Response({'Teams':ser.data})


class CreateTeamAPIView(generics.GenericAPIView):
    serializer_class = TeamSerializer

    @swagger_auto_schema(tags=['Teams'], operation_description='Creates a new team')
    def post(self, request, *args, **kwargs):
        data = request.data
        if models.Team.objects.filter(name=data['name']).exists():
            return Response({'message':'Team already exists'})
        try:
            if country_instance := models.Country.objects.get(name=data['country']):
                if int(data['score']) > 0:
                    models.Team.objects.create(name=data['name'], country=country_instance, score=data['score'])
                else:
                    return Response({'message':'Score can not be less than 0'})
        except models.Country.DoesNotExist:
            return Response({'message':'country not found'})
        return Response({'message':'Success', 'data':data}, status=status.HTTP_201_CREATED)


class UpdateTeamAPIView(generics.GenericAPIView):
    serializer_class = TeamSerializer

    @swagger_auto_schema(tags=['Teams'], operation_description='Update the details of a team')
    def put(self, request, id, *args, **kwargs):
        data = request.data
        team = get_team(id)
        try:
            country_id = models.Country.objects.filter(name=data['country'])[0].id
        except:
            return Response({'message':'Country not found, consider adding country first'},status=status.HTTP_404_NOT_FOUND)
        if team is None:
            return Response({'message':'Team with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Team.objects.filter(id=id).update(name=data['name'], country=country_id, score=data['score'])
        return Response({'message':'Successfully changed team details', 'data':data},status=status.HTTP_200_OK)


class DeleteTeamAPIView(generics.DestroyAPIView):
    serializer_class = TeamSerializer

    @swagger_auto_schema(tags=['Teams'], operation_description='deletes a team')
    def delete(self, request, id):
        try:
            models.Team.objects.get(id=id)
        except:
            return Response({'message':'Team with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Team.objects.filter(id=id).delete()
        return Response({'message':'success'}, status=status.HTTP_200_OK)


class GetPlayerAPIView(APIView):
    serlizer_class = PlayerSerializer

    @swagger_auto_schema(tags=['Players'], operation_description='List outs all the players')
    def get(self, request):
        player_qs = models.Player.objects.all()
        ser = self.serlizer_class(player_qs, many=True)
        return Response({'Players':ser.data})


class CreatePlayerAPIView(generics.GenericAPIView):
    serializer_class = PlayerSerializer

    @swagger_auto_schema(tags=['Players'], operation_description='Creates a new player')
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            if country_instance := models.Country.objects.get(name=data['country']):
                try:
                    if team_instance := models.Team.objects.get(name=data['team']):
                        models.Player.objects.create(name=data['name'], country=country_instance, team=team_instance, age=data['age'], total_runs=data['total_runs'], total_wickets=data['total_wickets'])
                except models.Team.DoesNotExist:
                    return Response({'message':'Team not found'})
        except models.Country.DoesNotExist:
            return Response({'message':'country not found'})
        return Response({'message':'Success', 'data':data},status=status.HTTP_200_OK)


class UpdatePlayerAPIView(generics.GenericAPIView):
    serializer_class = PlayerSerializer

    @swagger_auto_schema(tags=['Players'], operation_description='Update the details of a player')
    def put(self, request, id, *args, **kwargs):
        data = request.data
        player = get_player(id)
        try:
            country_id = get_country(data['country']).id
        except:
            return Response({'message':'Country not found, consider adding country first'},status=status.HTTP_404_NOT_FOUND)
        try:
            team_id = get_team(data['name']).id
        except:
            return Response({'message':'Team not found, consider adding team first'},status=status.HTTP_404_NOT_FOUND)
        if player is None:
            return Response({'message':'player with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        if (int(data['total_wickets'] < 0) or (int(data['total_runs'] < 0))):
            return Response({'message':'runs or wickets cannot be less than 0'}, status=status.HTTP_400_BAD_REQUEST)
        models.Player.objects.filter(id=id).update(name=data['name'], country=country_id, age=data['age'], total_runs=data['total_runs'], total_wickets=data['total_wickets'], team=team_id)
        return Response({'message':'Successfully changed player details', 'data':data},status=status.HTTP_200_OK)


class DeletePlayerAPIView(generics.DestroyAPIView):
    serializer_class = PlayerSerializer

    @swagger_auto_schema(tags=['Players'], operation_description='deletes a player')
    def delete(self, request, id):
        try:
            models.Player.objects.get(id=id)
        except:
            return Response({'message':'Player with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Player.objects.filter(id=id).delete()
        return Response({'message':'success'}, status=status.HTTP_200_OK)


class GetVenueAPIView(APIView):
    serlizer_class = VenueSerializer

    @swagger_auto_schema(tags=['Venue'], operation_description='List outs all the venues')
    def get(self, request):
        venue_qs = models.Venue.objects.all()
        ser = self.serlizer_class(venue_qs, many=True)
        return Response({'Venues':ser.data})


class CreateVenueAPIView(generics.GenericAPIView):
    serializer_class = VenueSerializer

    @swagger_auto_schema(tags=['Venue'], operation_description='Creates a new venue')
    def post(self, request, *args, **kwargs):
        data = request.data
        if models.Venue.objects.filter(place=data['place']).exists():
            if models.Country.objects.filter(name=data['country']).exists():
                return Response({'message':'venue already exists in the country'})
        if len(data['place']) > 0:
            try:
                if country_instance := models.Country.objects.get(name=data['country']):
                    models.Venue.objects.create(place=data['place'], country=country_instance)
            except models.Country.DoesNotExist:
                return Response({'message':'country not found'})
        else:
            return Response({'message':'Place can not be empty'})

        return Response({'message':'Success', 'data':data})


class UpdateVenueAPIView(generics.GenericAPIView):
    serializer_class = VenueSerializer

    @swagger_auto_schema(tags=['Venue'], operation_description='Creates a new venue')
    def put(self, request,id, *args, **kwargs):
        data = request.data
        venue = get_venue(id)
        if venue is None:
            return Response({'message':'venue with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        if len(data['place']) < 1:
            return Response({'message':'Place cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            country_id = get_country(data['country']).id
        except:
            return Response({'message':'Country not found, consider adding country first'},status=status.HTTP_404_NOT_FOUND)
        models.Venue.objects.filter(id=id).update(place=data['place'], country=country_id)
        return Response({'message':'Successfully changed venue details', 'data':data},status=status.HTTP_200_OK)


class DeleteVenueAPIView(generics.DestroyAPIView):
    serializer_class = VenueSerializer

    @swagger_auto_schema(tags=['Venue'], operation_description='deletes a venue')
    def delete(self, request, id):
        try:
            models.Venue.objects.get(id=id)
        except:
            return Response({'message':'Venue with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Venue.objects.filter(id=id).delete()
        return Response({'message':'success'}, status=status.HTTP_200_OK)


class GetMatchAPIView(APIView):
    serlizer_class = MatchSerializer

    @swagger_auto_schema(tags=['Match'], operation_description='List outs all the matches')
    def get(self, request):
        matches_qs = models.Match.objects.all()
        ser = self.serlizer_class(matches_qs, many=True)
        return Response({'Matches':ser.data})


class CreateMatchAPIView(generics.GenericAPIView):
    serializer_class = MatchSerializer

    @swagger_auto_schema(tags=['Match'], operation_description='Creates a new match')
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            player = models.Player.objects.get(name=data['player_of_match'])
        except models.Player.DoesNotExist:
            return Response({'message':'no such player found'})

        if str(data['winner'].lower()) == str(data['loser'].lower()):
            return Response({'message':'Winning team cant lose'})
        try:
            player_of_match_team = models.Player.objects.filter(name=data['player_of_match'])[0].team
        except:
            return Response({'message':'Player did not play the match'})
        try:
            winning_team = models.Team.objects.get(name=data['winner'])
        except:
            return Response({'message':'winning team not found'})
        try:
            losing_team = models.Team.objects.get(name=data['loser'])
        except:
            return Response({'message':'losing team not found'})
        try:
            player = models.Player.objects.get(name=data['player_of_match'])
        except:
            return Response({'message':'player of match not found'})
        try:
            bowler = models.Player.objects.get(name=data['bowler_of_match'])
        except:
            return Response({'message':'bowler of match not found'})
        try:
            fielder = models.Player.objects.get(name=data['fielder_of_match'])
        except:
            return Response({'message':'fielder of match not found'})
        if (data['winner_wickets'] < 0) or (data['loser_wickets'] < 0):
            return Response({'message':'Wickets cannot be negative'})
        if (data['winner_wickets'] > 10) or (data['loser_wickets'] > 10):
            return Response({'message':'Wickets cannot be more than 10'})
        if data['winner_score'] >= 0:
            if data['winner_score'] >= data['loser_score']:
                if str(player_of_match_team).lower() != str(data['winner']).lower():
                    return Response({'message':'Player of match has to be from winning team'})
        models.Match.objects.create(winner_score=data['winner_score'],loser_score=data['loser_score'],winner_wickets=data['winner_wickets'],loser_wickets=data['loser_wickets'],name=str(winning_team)+' vs '+str(losing_team), winner=winning_team, loser=losing_team, player_of_match=player,bowler_of_match=bowler, fielder_of_match=fielder)
        models.Team.objects.filter(name=data['winner']).update(score=F('score')+2)
        return Response({'message':'Success'})


class DeleteMatchAPIView(generics.DestroyAPIView):
    serializer_class = MatchSerializer

    @swagger_auto_schema(tags=['Match'], operation_description='deletes a match')
    def delete(self, request, id):
        try:
            models.Match.objects.get(id=id)
        except:
            return Response({'message':'Match with id {} not found'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        models.Match.objects.filter(id=id).delete()
        return Response({'message':'success'}, status=status.HTTP_200_OK)


class GetScoreAPIView(APIView):
    serlizer_class = ScoreSerializer

    @swagger_auto_schema(tags=['Scores'], operation_description='List outs scores of all teams')
    def get(self, request):
        matches_qs = models.Team.objects.all()
        ser = self.serlizer_class(matches_qs, many=True)
        return Response({'Scores':ser.data})


class GetResultsAPIView(APIView):
    serlizer_class = ScoreSerializer

    @swagger_auto_schema(tags=['Results'], operation_description='List outs results')
    def get(self, request):
        all_matches = {}
        matches_qs = models.Match.objects.all()
        for match in matches_qs:
            wickets_left = 11-int(match.winner_wickets)
            runs_left = int(match.winner_score) - int(match.loser_score)
            all_matches[match.name] = str(match.winner) + ' beat ' + str(match.loser) + ' by ' + str(wickets_left) + ' wickets'
        return Response(all_matches)