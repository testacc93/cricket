
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from cricketapp import views

urlpatterns = [
    path('countries', views.GetCountryAPIView.as_view(), name='countries'),
    path('country', views.CreateCountryAPIView.as_view(), name='create-country'),
    path('oldcountry/<id>', views.UpdateCountryAPIView.as_view(), name='update-country'),
    path('delcountry/<id>', views.DeleteCountryAPIView.as_view(), name='delete-country'),
    path('teams', views.GetTeamAPIView.as_view(), name='teams'),
    path('team', views.CreateTeamAPIView.as_view(), name='create-team'),
    path('oldteam/<id>', views.UpdateTeamAPIView.as_view(), name='create-team'),
    path('delteam/<id>', views.DeleteTeamAPIView.as_view(), name='delete-team'),
    path('players', views.GetPlayerAPIView.as_view(), name='players'),
    path('player', views.CreatePlayerAPIView.as_view(), name='create-player'),
    path('oldplayer/<id>', views.UpdatePlayerAPIView.as_view(), name='update-player'),
    path('delplayer/<id>', views.DeletePlayerAPIView.as_view(), name='delete-player'),
    path('venues', views.GetVenueAPIView.as_view(), name='venue'),
    path('venue', views.CreateVenueAPIView.as_view(), name='create-venue'),
    path('oldvenue/<id>', views.UpdateVenueAPIView.as_view(), name='update-venue'),
    path('delvenue/<id>', views.DeleteVenueAPIView.as_view(), name='delete-venue'),
    path('matches', views.GetMatchAPIView.as_view(), name='match'),
    path('match', views.CreateMatchAPIView.as_view(), name='create-match'),
    path('delmatch/<id>', views.DeleteMatchAPIView.as_view(), name='delete-match'),
    path('scores', views.GetScoreAPIView.as_view(), name='scores'),
    path('results', views.GetResultsAPIView.as_view(), name='result'),
]

