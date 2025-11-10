from rest_framework import serializers
from .models import Teams, Drivers, Circuits

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


'''
http://127.0.0.1:8000/api/teams/
http://127.0.0.1:8000/api/drivers/
http://127.0.0.1:8000/api/circuits/
http://127.0.0.1:8000/api/report/
'''