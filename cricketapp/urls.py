
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from cricketapp import views

urlpatterns = [
    # path('countries/<searchkey>', views.GetCountryAPIView.as_view(), name='countries'),
    path('countries/', views.GetCountryAPIView.as_view(), name='countries'),
    path('create-country', views.CreateCountryAPIView.as_view(), name='create-country'),


    path('teams', views.GetTeamAPIView.as_view(), name='teams'),
    path('create-team', views.CreateTeamAPIView.as_view(), name='create-team'),

    path('players', views.GetPlayerAPIView.as_view(), name='players'),
    path('create-player', views.CreatePlayerAPIView.as_view(), name='create-player'),

    path('venue', views.GetVenueAPIView.as_view(), name='venue'),
    path('create-venue', views.CreateVenueAPIView.as_view(), name='create-venue'),

    path('match', views.GetMatchAPIView.as_view(), name='match'),
    path('create-match', views.CreateMatchAPIView.as_view(), name='create-match'),

    path('scores', views.GetScoreAPIView.as_view(), name='scores'),

    path('result', views.GetResultsAPIView.as_view(), name='result'),

]

