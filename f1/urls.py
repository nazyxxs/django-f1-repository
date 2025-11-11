# Локальні маршрути API
from django.urls import path, include
from rest_framework import routers
from .views import TeamViewSet, DriverViewSet, CircuitViewSet, team_driver_report

router = routers.DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'circuits', CircuitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/', team_driver_report, name='team-driver-report'),
]
