# Реалізує CRUD та звіт
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count

from .models import (
    Teams, Drivers, Circuits, Principals, Cars,
    DriverTeamSeason, Races, Results, Seasons,
    ScoringSystem, YearChampion
)

from .serializers import (
    TeamSerializer, DriverSerializer, CircuitSerializer,
    PrincipalSerializer, CarSerializer, DriverTeamSeasonSerializer,
    RaceSerializer, ResultSerializer, SeasonSerializer,
    ScoringSystemSerializer, YearChampionSerializer
)

from .repositories import F1Repository

from django_filters.rest_framework import DjangoFilterBackend

repo = F1Repository()

# CRUD
class TeamViewSet(viewsets.ModelViewSet):
    queryset = repo.teams.list_all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['base_country', 'team_name']

class DriverViewSet(viewsets.ModelViewSet):
    queryset = repo.drivers.list_all()
    serializer_class = DriverSerializer

class CircuitViewSet(viewsets.ModelViewSet):
    queryset = repo.circuits.list_all()
    serializer_class = CircuitSerializer

class PrincipalViewSet(viewsets.ModelViewSet):
    queryset = Principals.objects.all()
    serializer_class = PrincipalSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer

class DriverTeamSeasonViewSet(viewsets.ModelViewSet):
    queryset = DriverTeamSeason.objects.all()
    serializer_class = DriverTeamSeasonSerializer

class RaceViewSet(viewsets.ModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultSerializer

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer

class ScoringSystemViewSet(viewsets.ModelViewSet):
    queryset = ScoringSystem.objects.all()
    serializer_class = ScoringSystemSerializer

class YearChampionViewSet(viewsets.ModelViewSet):
    queryset = YearChampion.objects.all()
    serializer_class = YearChampionSerializer


#   ЗВІТ
@api_view(['GET'])
def team_driver_report(request):
    data = (DriverTeamSeason.objects
            .values('team__team_name')
            .annotate(driver_count=Count('driver'))
            .order_by('-driver_count'))
    return Response(list(data))
