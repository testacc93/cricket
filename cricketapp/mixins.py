from cricketapp import models

def get_country(name):
    try:
        country = models.Country.objects.get(name=name)
    except models.Country.DoesNotExist:
        return None
    return country


def get_team(name):
    try:
        team = models.Team.objects.get(name=name)
    except models.Team.DoesNotExist:
        return None
    return team


def get_player(id):
    try:
        player = models.Player.objects.get(id=id)
    except models.Player.DoesNotExist:
        return None
    return player


def get_venue(id):
    try:
        venue = models.Venue.objects.get(id=id)
    except models.Venue.DoesNotExist:
        return None
    return venue
