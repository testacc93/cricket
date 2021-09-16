
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from cricketapp import views

urlpatterns = [
    path('countries', views.GetCountryAPIView.as_view(), name='countries'),
    path('teams', views.GetTeamAPIView.as_view(), name='teams'),
    path('players', views.GetPlayerAPIView.as_view(), name='players'),
    path('venues', views.GetVenueAPIView.as_view(), name='venues'),
    path('matches', views.GetMatchAPIView.as_view(), name='matches'),
    path('scores', views.GetScoreAPIView.as_view(), name='scores'),



]

