import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bokeh.embed import components
from bokeh.plotting import figure
from django.shortcuts import render
from .repositories import F1Repository
from bokeh.models import ColumnDataSource

repo = F1Repository()

def dashboard_v1(request):
    count_param = request.GET.get("count", "20")  # default = 20

    try:
        pilot_limit = int(count_param)
    except ValueError:
        pilot_limit = 20

    # 1. СЕРЕДНЯ КІЛЬКІСТЬ ОЧОК ПІЛОТІВ (Bar Chart)

    qs1 = repo.avg_points_per_driver().values("first_name", "last_name", "avg_points")
    df1 = pd.DataFrame(qs1)

    # Конвертація та очистка
    df1["avg_points"] = pd.to_numeric(df1["avg_points"], errors='coerce').fillna(0)
    df1["name"] = df1["first_name"] + " " + df1["last_name"]

    df1 = df1.sort_values(by="avg_points", ascending=False).head(pilot_limit)

    fig1 = px.bar(
        df1,
        x="name", y="avg_points",
        title=f"Топ-{pilot_limit} пілотів за середніми очками",
        labels={"avg_points": "Середні очки", "name": "Пілот"},
        text_auto='.1f'
    )
    fig1.update_layout(xaxis={'categoryorder': 'total descending'})

    # Фільтр для графіка перемог
    min_wins_param = request.GET.get("min_wins", "0")
    min_wins = int(min_wins_param)

    # 2. КІЛЬКІСТЬ ПЕРЕМОГ ПІЛОТІВ
    qs2 = repo.driver_wins().values("first_name", "last_name", "wins")
    df2 = pd.DataFrame(qs2)

    df2["wins"] = pd.to_numeric(df2["wins"], errors='coerce').fillna(0).astype(int)
    df2["name"] = df2["first_name"] + " " + df2["last_name"]

    df2 = df2[df2["wins"] >= min_wins]

    # Сортування
    df2_top = df2.sort_values(by="wins", ascending=False)

    # Побудова графіка
    fig2 = go.Figure(
        data=[
            go.Bar(
                x=df2_top['name'],
                y=df2_top['wins'],
                text=df2_top['wins'],
                textposition='auto',
                marker_color='royalblue'
            )
        ]
    )
    fig2.update_layout(
        title=f"Пілоти з кількістю перемог ≥ {min_wins}",
        xaxis_title="Пілот",
        yaxis_title="Перемоги",
    )

    # 3. КІЛЬКІСТЬ ГОНОК НА ТРАСАХ (Line Chart)

    qs3 = repo.races_per_circuit().values("circuit_id", "circuit_name", "race_count")
    df3 = pd.DataFrame(qs3)
    df3["race_count"] = pd.to_numeric(df3["race_count"], errors='coerce').fillna(0)

    df3 = df3.sort_values(by="race_count", ascending=False).head(15)

    fig3 = px.line(
        df3,
        x="circuit_name", y="race_count",
        markers=True,  # Додає точки на лінії
        title="Топ трас за кількістю проведених гонок (Лінійний графік)",
        labels={"race_count": "К-сть гонок", "circuit_name": "Траса"}
    )


    # 4. ЗАГАЛЬНІ ОЧКИ КОМАНД

    qs4 = repo.team_total_points().values("team_name", "total_points")
    df4 = pd.DataFrame(qs4)
    df4["total_points"] = pd.to_numeric(df4["total_points"], errors='coerce').fillna(0)

    # Беру топ 10, можна по суті змінити
    df4_top = df4.sort_values(by="total_points", ascending=False).head(10)

    fig4 = px.pie(
        df4_top,
        values="total_points",
        names="team_name",
        title="Частка очок топ-10 команд (Кругова діаграма)",
        hole=0.3  # Типу пончик (просто для краси)
    )

    # 5. ПІЛОТИ, ЯКІ ВИСТУПАЛИ У >1 КОМАНДІ (Bar Chart)

    qs5 = repo.drivers_in_multiple_teams().values("first_name", "last_name", "teams_count")
    df5 = pd.DataFrame(qs5)
    df5["teams_count"] = pd.to_numeric(df5["teams_count"], errors='coerce').fillna(0)
    df5["name"] = df5["first_name"] + " " + df5["last_name"]

    df5 = df5.sort_values(by="teams_count", ascending=False).head(20)

    fig5 = px.bar(
        df5,
        x="name", y="teams_count",
        title="Пілоти з найбільшою кількістю команд",
        labels={"teams_count": "Кількість команд", "name": "Пілот"},
        text_auto=True
    )
    fig5.update_layout(xaxis={'categoryorder': 'total descending'})


    # 6. ТОП-3 КОМАНД ЗА СУМОЮ ОЧОК (Bar Chart - Horizontal)

    qs6 = repo.top3_teams_by_points().values("team_name", "total_points")
    df6 = pd.DataFrame(qs6)
    df6["total_points"] = pd.to_numeric(df6["total_points"], errors='coerce').fillna(0)

    fig6 = px.bar(
        df6,
        x="total_points", y="team_name",
        orientation='h',
        title="Топ-3 команди (Горизонтальний графік)",
        labels={"total_points": "Очки", "team_name": "Команда"},
        text_auto=True
    )

    # Повертаємо HTML
    return render(request, "dashboard/dashboard_v1.html", {
        "chart1": fig1.to_html(full_html=False),
        "chart2": fig2.to_html(full_html=False),
        "chart3": fig3.to_html(full_html=False),
        "chart4": fig4.to_html(full_html=False),
        "chart5": fig5.to_html(full_html=False),
        "chart6": fig6.to_html(full_html=False),
        "selected_count": count_param,
        "selected_min_wins": min_wins_param,
    })


def dashboard_v2(request):
    # 1) Середня кількість очок пілотів (Bar)

    qs1 = repo.avg_points_per_driver().values("first_name", "last_name", "avg_points")
    df1 = pd.DataFrame(qs1)
    df1["avg_points"] = pd.to_numeric(df1["avg_points"], errors="coerce").fillna(0)
    df1["name"] = df1["first_name"] + " " + df1["last_name"]
    df1 = df1.sort_values(by="avg_points", ascending=False).head(20)

    source1 = ColumnDataSource(df1)
    p1 = figure(
        x_range=list(df1["name"]),
        height=400,
        title="Середня кількість очок пілотів",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p1.vbar(x="name", top="avg_points", width=0.9, source=source1)
    p1.xaxis.major_label_orientation = 1.1
    p1.xaxis.axis_label = "Пілот"
    p1.yaxis.axis_label = "Середні очки"


    # 2) Кількість перемог пілотів (Bar)

    qs2 = repo.driver_wins().values("first_name", "last_name", "wins")
    df2 = pd.DataFrame(qs2)
    df2["wins"] = pd.to_numeric(df2["wins"], errors="coerce").fillna(0).astype(int)
    df2["name"] = df2["first_name"] + " " + df2["last_name"]
    df2 = df2.sort_values(by="wins", ascending=False).head(20)

    source2 = ColumnDataSource(df2)
    p2 = figure(
        x_range=list(df2["name"]),
        height=400,
        title="Кількість перемог пілотів",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p2.vbar(x="name", top="wins", width=0.9, source=source2)
    p2.xaxis.major_label_orientation = 1.1
    p2.xaxis.axis_label = "Пілот"
    p2.yaxis.axis_label = "Перемоги"


    # 3) Кількість гонок на трасах (Line)

    qs3 = repo.races_per_circuit().values("circuit_name", "race_count")
    df3 = pd.DataFrame(qs3)
    df3["race_count"] = pd.to_numeric(df3["race_count"], errors="coerce").fillna(0)
    df3 = df3.sort_values(by="race_count", ascending=False)

    source3 = ColumnDataSource(df3)
    p3 = figure(
        x_range=list(df3["circuit_name"]),
        height=400,
        title="Кількість гонок на трасах",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p3.line(x="circuit_name", y="race_count", source=source3, line_width=2)
    p3.circle(x="circuit_name", y="race_count", source=source3, size=8)
    p3.xaxis.major_label_orientation = 1.1
    p3.xaxis.axis_label = "Траса"
    p3.yaxis.axis_label = "К-сть гонок"


    # 4) Загальні очки команд (Bar)

    qs4 = repo.team_total_points().values("team_name", "total_points")
    df4 = pd.DataFrame(qs4)
    df4["total_points"] = pd.to_numeric(df4["total_points"], errors="coerce").fillna(0)
    df4 = df4.sort_values(by="total_points", ascending=False)

    source4 = ColumnDataSource(df4)
    p4 = figure(
        x_range=list(df4["team_name"]),
        height=400,
        title="Загальні очки команд",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p4.vbar(x="team_name", top="total_points", width=0.9, source=source4)
    p4.xaxis.major_label_orientation = 1.1
    p4.xaxis.axis_label = "Команда"
    p4.yaxis.axis_label = "Очки"


    # 5) Пілоти, які виступали у >1 команді (Bar)

    qs5 = repo.drivers_in_multiple_teams().values("first_name", "last_name", "teams_count")
    df5 = pd.DataFrame(qs5)
    df5["teams_count"] = pd.to_numeric(df5["teams_count"], errors="coerce").fillna(0)
    df5["name"] = df5["first_name"] + " " + df5["last_name"]
    df5 = df5.sort_values(by="teams_count", ascending=False)

    source5 = ColumnDataSource(df5)
    p5 = figure(
        x_range=list(df5["name"]),
        height=400,
        title="Пілоти, які виступали у більше ніж 1 команді",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p5.vbar(x="name", top="teams_count", width=0.9, source=source5)
    p5.xaxis.major_label_orientation = 1.1
    p5.xaxis.axis_label = "Пілот"
    p5.yaxis.axis_label = "К-сть команд"


    # 6) Топ-3 команди за сумою очок (Horizontal Bar)

    qs6 = repo.top3_teams_by_points().values("team_name", "total_points")
    df6 = pd.DataFrame(qs6)
    df6["total_points"] = pd.to_numeric(df6["total_points"], errors="coerce").fillna(0)

    source6 = ColumnDataSource(df6)
    p6 = figure(
        y_range=list(df6["team_name"]),
        height=300,
        title="Топ-3 команди за сумою очок",
        toolbar_location="above",
        sizing_mode="stretch_width",
    )
    p6.hbar(y="team_name", right="total_points", height=0.6, source=source6)
    p6.xaxis.axis_label = "Очки"
    p6.yaxis.axis_label = "Команда"

    # Вмонтування Bokeh у Django-шаблон
    script, divs = components({
        "chart1": p1,
        "chart2": p2,
        "chart3": p3,
        "chart4": p4,
        "chart5": p5,
        "chart6": p6,
    })

    return render(request, "dashboard/dashboard_v2.html", {
        "bokeh_script": script,
        "chart1": divs["chart1"],
        "chart2": divs["chart2"],
        "chart3": divs["chart3"],
        "chart4": divs["chart4"],
        "chart5": divs["chart5"],
        "chart6": divs["chart6"],
    })