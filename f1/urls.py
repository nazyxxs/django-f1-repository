from django.urls import path, include
from rest_framework import routers

from .views import (
    TeamViewSet, DriverViewSet, CircuitViewSet,
    PrincipalViewSet, CarViewSet, DriverTeamSeasonViewSet,
    RaceViewSet, ResultViewSet, SeasonViewSet,
    ScoringSystemViewSet, YearChampionViewSet,
    team_driver_report, remote_cars_page, remote_clients_page
)
from .views import (
    remote_cars, remote_clients,
    remote_cars_delete, remote_clients_delete
)

router = routers.DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'circuits', CircuitViewSet)
router.register(r'principals', PrincipalViewSet)
router.register(r'cars', CarViewSet)
router.register(r'dts', DriverTeamSeasonViewSet)
router.register(r'races', RaceViewSet)
router.register(r'results', ResultViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'scoring', ScoringSystemViewSet)
router.register(r'champions', YearChampionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/', team_driver_report, name='team-driver-report'),
    path('remote/cars/', remote_cars, name='remote_cars'),
    path('remote/cars/delete/<int:pk>/', remote_cars_delete, name='remote_cars_delete'),
    path("remote/cars/page/", remote_cars_page, name="remote_cars_page"),
    path('remote/clients/', remote_clients, name='remote_clients'),
    path('remote/clients/delete/<int:pk>/', remote_clients_delete, name='remote_clients_delete'),
    path("remote/clients/page/", remote_clients_page, name="remote_clients_page"),
]
