from typing import Generic, TypeVar, Type, Optional, Iterable
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count, Sum, Q

from .models import (
    Teams, Principals, Drivers, DriverTeamSeason, Cars,
    Circuits, Seasons, Races, Results, ScoringSystem, YearChampion
)

T = TypeVar("T", bound=models.Model)

# BASE REPOSITORY

class BaseRepository(Generic[T]):
    def list_all(self) -> Iterable[T]:
        raise NotImplementedError

    def get_by_id(self, obj_id: int) -> Optional[T]:
        raise NotImplementedError

    def add(self, **fields) -> T:
        raise NotImplementedError

    def delete_by_id(self, obj_id: int) -> bool:
        raise NotImplementedError


class DjangoRepository(BaseRepository[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def list_all(self) -> Iterable[T]:
        return self.model.objects.all()

    def get_by_id(self, obj_id: int) -> Optional[T]:
        try:
            return self.model.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            return None

    def add(self, **fields) -> T:
        obj = self.model(**fields)
        obj.save()
        return obj

    def delete_by_id(self, obj_id: int) -> bool:
        try:
            obj = self.model.objects.get(pk=obj_id)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            return False


# ENTITY REPOSITORIES

class TeamRepository(DjangoRepository[Teams]):
    def __init__(self):
        super().__init__(Teams)

class PrincipalRepository(DjangoRepository[Principals]):
    def __init__(self):
        super().__init__(Principals)

class DriverRepository(DjangoRepository[Drivers]):
    def __init__(self):
        super().__init__(Drivers)

class DriverTeamSeasonRepository(DjangoRepository[DriverTeamSeason]):
    def __init__(self):
        super().__init__(DriverTeamSeason)

class CarRepository(DjangoRepository[Cars]):
    def __init__(self):
        super().__init__(Cars)

class CircuitRepository(DjangoRepository[Circuits]):
    def __init__(self):
        super().__init__(Circuits)

class SeasonRepository(DjangoRepository[Seasons]):
    def __init__(self):
        super().__init__(Seasons)

class RaceRepository(DjangoRepository[Races]):
    def __init__(self):
        super().__init__(Races)

class ResultRepository(DjangoRepository[Results]):
    def __init__(self):
        super().__init__(Results)

class ScoringSystemRepository(DjangoRepository[ScoringSystem]):
    def __init__(self):
        super().__init__(ScoringSystem)

class YearChampionRepository(DjangoRepository[YearChampion]):
    def __init__(self):
        super().__init__(YearChampion)


# MAIN F1 REPOSITORY

class F1Repository:
    def __init__(self):
        self.teams = TeamRepository()
        self.principals = PrincipalRepository()
        self.drivers = DriverRepository()
        self.driver_team_season = DriverTeamSeasonRepository()
        self.cars = CarRepository()
        self.circuits = CircuitRepository()
        self.seasons = SeasonRepository()
        self.races = RaceRepository()
        self.results = ResultRepository()
        self.scoring_system = ScoringSystemRepository()
        self.year_champions = YearChampionRepository()

    # 1) Середня кількість очок кожного пілота за всі гонки
    def avg_points_per_driver(self):
        return (Drivers.objects
                .annotate(
                    total_points=Sum("results__points"),
                    avg_points=Avg("results__points"),
                    race_count=Count("results__result_id")
                )
                .filter(race_count__gt=0)
                .order_by("-avg_points"))

    # 2) Кількість перемог по кожному пілоту (position = 1)
    def driver_wins(self):
        return (Drivers.objects
                .annotate(
                    wins=Count("results", filter=Q(results__position=1))
                )
                .filter(wins__gt=0)
                .order_by("-wins"))

    # 3) Скільки гонок проведено на кожній трасі
    def races_per_circuit(self):
        return (Circuits.objects
                .annotate(race_count=Count("races"))
                .filter(race_count__gt=0)
                .order_by("-race_count"))

    # 4) Загальна кількість очок у команди
    def team_total_points(self):
        return (Teams.objects
            .annotate(
                total_points=Sum("driverteamseason__driver__results__points")
            )
            .filter(total_points__isnull=False)
            .order_by("-total_points")
        )

    # 5) Пілоти, які виступали у більше ніж одній команді
    def drivers_in_multiple_teams(self):
        return (Drivers.objects
                .annotate(
                    teams_count=Count("driverteamseason__team_id", distinct=True)
                )
                .filter(teams_count__gt=1)
                .order_by("-teams_count"))

    # 6) Топ-3 команди за сумою очок їхніх пілотів
    def top3_teams_by_points(self):
        return (Teams.objects
            .annotate(
                total_points=Sum("driverteamseason__driver__results__points")
            )
            .filter(total_points__isnull=False)
            .order_by("-total_points")[:3]
        )
