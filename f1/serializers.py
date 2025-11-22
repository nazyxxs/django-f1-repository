# Перетворює моделі в JSON
from rest_framework import serializers
from .models import (
    Teams, Drivers, Circuits, Principals, Cars,
    DriverTeamSeason, Races, Results, Seasons,
    ScoringSystem, YearChampion
)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'

class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuits
        fields = '__all__'

class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principals
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'

class DriverTeamSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverTeamSeason
        fields = '__all__'

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Races
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = '__all__'

class ScoringSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringSystem
        fields = '__all__'

class YearChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearChampion
        fields = '__all__'

'''
http://127.0.0.1:8000/api/teams/
http://127.0.0.1:8000/api/drivers/
http://127.0.0.1:8000/api/circuits/
http://127.0.0.1:8000/api/report/
'''