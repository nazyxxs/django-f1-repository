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
from django.urls import path
from . import views_stats
from .views_dashboard import dashboard_v1, dashboard_v2

from .views_parallel import parallel_test

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

    # === 1 TASK ===
    path("stats/drivers/avg-points/", views_stats.avg_points_per_driver_view),
    path("stats/drivers/wins/", views_stats.driver_wins_view),
    path("stats/circuits/races/", views_stats.races_per_circuit_view),
    path("stats/teams/total-points/", views_stats.team_total_points_view),
    path("stats/drivers/multi-team/", views_stats.drivers_in_multiple_teams_view),
    path("stats/teams/top3/", views_stats.top3_teams_by_points_view),


    # === TASK 2 ===
    path("stats/basic/positions/", views_stats.statistics_positions_view),
    path("stats/basic/track-length/", views_stats.statistics_track_length_view),
    path("stats/group/driver-position/", views_stats.group_average_position_per_driver),
    path("stats/group/track-length-country/", views_stats.group_avg_track_length_by_country),
    path("stats/group/points-season/", views_stats.group_avg_points_by_season),


    # === TASK 3 ===
    path("dashboard/v1/", dashboard_v1, name="dashboard_v1"),
    path("api/dashboard/v2/", dashboard_v2, name="dashboard_v2"),


    # === TASK 4 ===
    path("dashboard/parallel/", parallel_test, name="parallel_test"),
]
