# Реалізує CRUD та звіт
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import render

from .NetworkHelper import NetworkHelper
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


# підключення до віддаленого API колеги
remote_api = NetworkHelper(
    base_url="http://127.0.0.1:8001/api",
    username="student2",
    password="UserTest!9"
)

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



#   REMOTE API — CARS
@api_view(['GET', 'POST'])
def remote_cars(request):
    if request.method == 'GET':
        status_code, data = remote_api.get_list("cars")
        return Response(data, status=status_code)

    if request.method == 'POST':
        status_code, data = remote_api.create_item("cars", request.data)
        return Response(data, status=status_code)


@api_view(['POST', 'DELETE'])
def remote_cars_delete(request, pk):
    status_code = remote_api.delete_item("cars", pk)
    return Response(status=status_code)


def remote_cars_page(request):
    status_code, cars = remote_api.get_list("cars")
    return render(request, "frontend/remote_cars.html", {"cars": cars})


#   REMOTE API — CLIENTS
@api_view(['GET', 'POST'])
def remote_clients(request):
    if request.method == 'GET':
        status_code, data = remote_api.get_list("clients")
        return Response(data, status=status_code)

    if request.method == 'POST':
        status_code, data = remote_api.create_item("clients", request.data)
        return Response(data, status=status_code)


@api_view(['POST', 'DELETE'])   # <--- важливо!
def remote_clients_delete(request, pk):
    status_code = remote_api.delete_item("clients", pk)
    return Response(status=status_code)


def remote_clients_page(request):
    status_code, clients = remote_api.get_list("clients")
    return render(request, "frontend/remote_clients.html", {"clients": clients})


