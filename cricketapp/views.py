
from django.shortcuts import render
from rest_framework.serializers import Serializer, SerializerMetaclass
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework import generics,status, exceptions
from cricketapp.models import Country, Team, Player
from cricketapp.serializers import CountrySerializer, TeamSerializer, PlayerSerializer, VenueSerializer, MatchSerializer, ScoreSerializer

from cricketapp import models


class GetCountryAPIView(APIView):
    serlizer_class = CountrySerializer

    @swagger_auto_schema(tags=['Get countries'], operation_description='List outs all countries')
    def get(self, request):
        countries_qs = models.Country.objects.all()
        ser = self.serlizer_class(countries_qs, many=True)
        return Response({'Countries':ser.data})


class GetTeamAPIView(APIView):
    serlizer_class = TeamSerializer

    @swagger_auto_schema(tags=['Get teams'], operation_description='List outs all the teams')
    def get(self, request):
        team_qs = models.Team.objects.all()
        ser = self.serlizer_class(team_qs, many=True)
        return Response({'Teams':ser.data})


class GetPlayerAPIView(APIView):
    serlizer_class = PlayerSerializer

    @swagger_auto_schema(tags=['Get players'], operation_description='List outs all the teams')
    def get(self, request):
        player_qs = models.Player.objects.all()
        ser = self.serlizer_class(player_qs, many=True)
        return Response({'Players':ser.data})


class GetVenueAPIView(APIView):
    serlizer_class = VenueSerializer

    @swagger_auto_schema(tags=['Get Venues'], operation_description='List outs all the teams')
    def get(self, request):
        venue_qs = models.Venue.objects.all()
        ser = self.serlizer_class(venue_qs, many=True)
        return Response({'Venues':ser.data})


class GetMatchAPIView(APIView):
    serlizer_class = MatchSerializer

    @swagger_auto_schema(tags=['Get Matches'], operation_description='List outs all the teams')
    def get(self, request):
        matches_qs = models.Match.objects.all()
        ser = self.serlizer_class(matches_qs, many=True)
        return Response({'Matches':ser.data})


class GetScoreAPIView(APIView):
    serlizer_class = ScoreSerializer

    @swagger_auto_schema(tags=['Get Scores'], operation_description='List outs all the teams')
    def get(self, request):
        matches_qs = models.Team.objects.all()
        ser = self.serlizer_class(matches_qs, many=True)
        return Response({'Scores':ser.data})



        