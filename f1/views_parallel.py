import time
import pandas as pd
from django.db import connection
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px

TOTAL_TASKS = 200  # К-сть запитів


# 1. SQL-функція для паралельного запуску
def count_races():
    # підрахунок кількості гонок
    start = time.time()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Races;")
        _ = cursor.fetchone()[0]

    return time.time() - start


# 2. Бенчмарк потоків
def benchmark_threads():
    thread_options = [1, 2, 4, 8, 16]
    results = []

    for n_threads in thread_options:
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [executor.submit(count_races) for _ in range(TOTAL_TASKS)]
            times = [f.result() for f in futures]

        avg_time = sum(times) / len(times)

        results.append({
            "threads": n_threads,
            "avg_time": avg_time
        })

    return pd.DataFrame(results)


# 3. Побудова графіка
def make_benchmark_chart(df):
    fig = px.line(
        df,
        x="threads",
        y="avg_time",
        markers=True,
        title=f"Час виконання {TOTAL_TASKS} SQL-запитів залежно від кількості потоків",
        labels={"threads": "Потоки", "avg_time": "Середній час (сек)"}
    )
    fig.update_traces(line=dict(width=3))
    return fig.to_html(full_html=False)


# 4. Django View
def parallel_test(request):
    df = benchmark_threads()
    chart = make_benchmark_chart(df)

    return render(request, "dashboard/parallel_test.html", {
        "chart": chart
    })
