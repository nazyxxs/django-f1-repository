from typing import Generic, TypeVar, Type, Optional, Iterable
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Teams, Principals, Drivers, DriverTeamSeason, Cars,
    Circuits, Seasons, Races, Results, ScoringSystem, YearChampion
)

T = TypeVar("T", bound=models.Model)


# Базові класи
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


# Репозиторії
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


# Точка доступу до всіх
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
