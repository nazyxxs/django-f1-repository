from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Teams, Drivers, Circuits, DriverTeamSeason
from .serializers import TeamSerializer, DriverSerializer, CircuitSerializer
from .repositories import F1Repository
from django_filters.rest_framework import DjangoFilterBackend

repo = F1Repository()

# CRUD для команд
class TeamViewSet(viewsets.ModelViewSet):
    queryset = repo.teams.list_all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['base_country', 'team_name']

# CRUD для пілотів
class DriverViewSet(viewsets.ModelViewSet):
    queryset = repo.drivers.list_all()
    serializer_class = DriverSerializer

# CRUD для трас
class CircuitViewSet(viewsets.ModelViewSet):
    queryset = repo.circuits.list_all()
    serializer_class = CircuitSerializer

# Звіт: кількість пілотів у кожній команді
@api_view(['GET'])
def team_driver_report(request):
    data = (DriverTeamSeason.objects
            .values('team__team_name')
            .annotate(driver_count=Count('driver'))
            .order_by('-driver_count'))
    return Response(list(data))
