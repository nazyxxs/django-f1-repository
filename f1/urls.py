from django.urls import path, include
from rest_framework import routers

from .views import (
    TeamViewSet, DriverViewSet, CircuitViewSet,
    PrincipalViewSet, CarViewSet, DriverTeamSeasonViewSet,
    RaceViewSet, ResultViewSet, SeasonViewSet,
    ScoringSystemViewSet, YearChampionViewSet,
    team_driver_report
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
]
