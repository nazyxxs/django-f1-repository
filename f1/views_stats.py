import pandas as pd
from django.http import JsonResponse

from .models import Results, Circuits
from .repositories import F1Repository

repo = F1Repository()

# конвертація queryset
def qs_to_dataframe(queryset, fields: list):
    data = list(queryset.values(*fields))
    df = pd.DataFrame(data)
    return df

# 1) Середня кількість очок кожного пілота
def avg_points_per_driver_view(request):
    qs = repo.avg_points_per_driver()

    df = qs_to_dataframe(qs, [
        "driver_id", "first_name", "last_name",
        "total_points", "avg_points", "race_count"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


# 2) Кількість перемог кожного пілота
def driver_wins_view(request):
    qs = repo.driver_wins()

    df = qs_to_dataframe(qs, [
        "driver_id", "first_name", "last_name", "wins"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


# 3) Кількість гонок на кожній трасі
def races_per_circuit_view(request):
    qs = repo.races_per_circuit()

    df = qs_to_dataframe(qs, [
        "circuit_id", "circuit_name", "race_count"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


# 4) Загальна кількість очок у команди
def team_total_points_view(request):
    qs = repo.team_total_points()

    df = qs_to_dataframe(qs, [
        "team_id", "team_name", "total_points"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


# 5) Пілоти, які виступали у більше ніж 1 команді
def drivers_in_multiple_teams_view(request):
    qs = repo.drivers_in_multiple_teams()

    df = qs_to_dataframe(qs, [
        "driver_id", "first_name", "last_name", "teams_count"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


# 6) Топ-3 команди за сумою очок
def top3_teams_by_points_view(request):
    qs = repo.top3_teams_by_points()

    df = qs_to_dataframe(qs, [
        "team_id", "team_name", "total_points"
    ])

    return JsonResponse(df.to_dict(orient="records"), safe=False)


def statistics_positions_view(request):
    qs = Results.objects.values("position")
    df = pd.DataFrame(qs)

    stats = {
        "mean": float(df["position"].mean()),
        "median": float(df["position"].median()),
        "min": int(df["position"].min()),
        "max": int(df["position"].max()),
    }

    return JsonResponse(stats, safe=False)



def statistics_track_length_view(request):
    qs = Circuits.objects.values("length_km")
    df = pd.DataFrame(qs)

    stats = {
        "mean": float(df["length_km"].mean()),
        "median": float(df["length_km"].median()),
        "min": float(df["length_km"].min()),
        "max": float(df["length_km"].max()),
    }

    return JsonResponse(stats, safe=False)

# Середня позиція пілотів
def group_average_position_per_driver(request):
    qs = Results.objects.values("driver_id", "driver__first_name", "driver__last_name", "position")
    df = pd.DataFrame(qs)

    grouped = (
        df.groupby(["driver_id", "driver__first_name", "driver__last_name"])["position"]
          .mean()
          .reset_index()
          .rename(columns={"position": "avg_position"})
    )

    return JsonResponse(grouped.to_dict(orient="records"), safe=False)

# Середня довжина трас по країнах
def group_avg_track_length_by_country(request):
    qs = Circuits.objects.values("country", "length_km")
    df = pd.DataFrame(qs)

    grouped = (
        df.groupby("country")["length_km"]
          .mean()
          .reset_index()
          .rename(columns={"length_km": "avg_length"})
    )

    return JsonResponse(grouped.to_dict(orient="records"), safe=False)

# Середні очки по сезонах
def group_avg_points_by_season(request):
    qs = Results.objects.values(
        "points",
        "race__season_year",
    )
    df = pd.DataFrame(qs)

    grouped = (
        df.groupby("race__season_year")["points"]
          .mean()
          .reset_index()
          .rename(columns={"points": "avg_points"})
    )

    return JsonResponse(grouped.to_dict(orient="records"), safe=False)

