from django.db import models


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    base_country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Teams'

    def __str__(self):
        return f"{self.team_name} ({self.base_country})"


class Principals(models.Model):
    principal_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='team_id', blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Principals'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Drivers(models.Model):
    driver_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Drivers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriverTeamSeason(models.Model):
    dts_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey('Drivers', models.DO_NOTHING, db_column='driver_id', blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='team_id', blank=True, null=True)
    season_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Driver_Team_Season'


class Cars(models.Model):
    car_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    year = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='team_id', blank=True, null=True)
    season_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cars'


class Circuits(models.Model):
    circuit_id = models.AutoField(primary_key=True)
    circuit_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    length_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Circuits'

    def __str__(self):
        return f"{self.circuit_name} ({self.country})"


class Seasons(models.Model):
    season_year = models.IntegerField(primary_key=True)
    scoring_system_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seasons'


class Races(models.Model):
    race_id = models.AutoField(primary_key=True)
    circuit = models.ForeignKey('Circuits', models.DO_NOTHING, db_column='circuit_id')
    season_year = models.IntegerField(blank=True, null=True)
    race_date = models.DateField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'Races'


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)
    race = models.ForeignKey('Races', models.DO_NOTHING, db_column='race_id', blank=True, null=True)
    driver = models.ForeignKey('Drivers', models.DO_NOTHING, db_column='driver_id', blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.driver} — {self.race} (Pos: {self.position}, Points: {self.points})"

    class Meta:
        managed = False
        db_table = 'Results'


class ScoringSystem(models.Model):
    system_id = models.AutoField(primary_key=True)
    season_year = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Scoring_System'


class YearChampion(models.Model):
    yc_id = models.AutoField(primary_key=True)
    season_year = models.IntegerField(blank=True, null=True)
    driver = models.ForeignKey('Drivers', models.DO_NOTHING, db_column='driver_id', blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='team_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Year_Champion'
