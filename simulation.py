import numpy as np
import pandas as pd
from collections import defaultdict

current_stats = {
    'MKS Siechnice': {'pts': 28, 'att': 5.10, 'def': 1.82},
    'Polonia Godzikowice': {'pts': 5, 'att': 1.18, 'def': 4.55},
    'Orzeł Święta Katarzyna': {'pts': 13, 'att': 3.09, 'def': 3.64},
    'Zorza Niemil': {'pts': 8, 'att': 1.82, 'def': 2.55},
    'Sokół II Marcinkowice': {'pts': 19, 'att': 3.55, 'def': 2.82},
    'Burza Chwalibożyce': {'pts': 21, 'att': 3.91, 'def': 3.18},
    'Czarni Sobocisko': {'pts': 26, 'att': 4.55, 'def': 1.64},
    'Lotos Gaj Oławski': {'pts': 17, 'att': 2.45, 'def': 2.91},
    'Jankowianka Wierzbno': {'pts': 5, 'att': 1.64, 'def': 4.55},
    'Moto Jelcz II Oława': {'pts': 19, 'att': 4.64, 'def': 2.09},
    'Odra Kotowice': {'pts': 10, 'att': 1.36, 'def': 2.55},
    'Szaluna Zębice': {'pts': 16, 'att': 2.91, 'def': 3.55}
}

# pozostałe kolejki
fixtures = [
    # Kolejka 12
    ('MKS Siechnice', 'Polonia Godzikowice'), ('Orzeł Święta Katarzyna', 'Zorza Niemil'),
    ('Sokół II Marcinkowice', 'Burza Chwalibożyce'), ('Czarni Sobocisko', 'Lotos Gaj Oławski'),
    ('Jankowianka Wierzbno', 'Moto Jelcz II Oława'), ('Odra Kotowice', 'Szaluna Zębice'),
    # Kolejka 13
    ('Odra Kotowice', 'MKS Siechnice'), ('Szaluna Zębice', 'Jankowianka Wierzbno'),
    ('Moto Jelcz II Oława', 'Czarni Sobocisko'), ('Lotos Gaj Oławski', 'Sokół II Marcinkowice'),
    ('Burza Chwalibożyce', 'Orzeł Święta Katarzyna'), ('Zorza Niemil', 'Polonia Godzikowice'),
    # Kolejka 14
    ('MKS Siechnice', 'Zorza Niemil'), ('Polonia Godzikowice', 'Burza Chwalibożyce'),
    ('Orzeł Święta Katarzyna', 'Lotos Gaj Oławski'), ('Sokół II Marcinkowice', 'Moto Jelcz II Oława'),
    ('Czarni Sobocisko', 'Szaluna Zębice'), ('Jankowianka Wierzbno', 'Odra Kotowice'),
    # Kolejka 15
    ('Czarni Sobocisko', 'Odra Kotowice'), ('Jankowianka Wierzbno', 'MKS Siechnice'),
    ('Szaluna Zębice', 'Sokół II Marcinkowice'), ('Moto Jelcz II Oława', 'Orzeł Święta Katarzyna'),
    ('Lotos Gaj Oławski', 'Polonia Godzikowice'), ('Burza Chwalibożyce', 'Zorza Niemil'),
    # Kolejka 16
    ('MKS Siechnice', 'Burza Chwalibożyce'), ('Zorza Niemil', 'Lotos Gaj Oławski'),
    ('Polonia Godzikowice', 'Moto Jelcz II Oława'), ('Orzeł Święta Katarzyna', 'Szaluna Zębice'),
    ('Sokół II Marcinkowice', 'Odra Kotowice'), ('Czarni Sobocisko', 'Jankowianka Wierzbno'),
    # Kolejka 17
    ('Czarni Sobocisko', 'MKS Siechnice'), ('Jankowianka Wierzbno', 'Sokół II Marcinkowice'),
    ('Odra Kotowice', 'Orzeł Święta Katarzyna'), ('Szaluna Zębice', 'Polonia Godzikowice'),
    ('Moto Jelcz II Oława', 'Zorza Niemil'), ('Lotos Gaj Oławski', 'Burza Chwalibożyce'),
    # Kolejka 18
    ('MKS Siechnice', 'Lotos Gaj Oławski'), ('Burza Chwalibożyce', 'Moto Jelcz II Oława'),
    ('Zorza Niemil', 'Szaluna Zębice'), ('Polonia Godzikowice', 'Odra Kotowice'),
    ('Orzeł Święta Katarzyna', 'Jankowianka Wierzbno'), ('Sokół II Marcinkowice', 'Czarni Sobocisko'),
    # Kolejka 19
    ('Burza Chwalibożyce', 'Szaluna Zębice'), ('Sokół II Marcinkowice', 'MKS Siechnice'),
    ('Czarni Sobocisko', 'Orzeł Święta Katarzyna'), ('Jankowianka Wierzbno', 'Polonia Godzikowice'),
    ('Odra Kotowice', 'Zorza Niemil'), ('Moto Jelcz II Oława', 'Lotos Gaj Oławski'),
    # Kolejka 20
    ('MKS Siechnice', 'Moto Jelcz II Oława'), ('Lotos Gaj Oławski', 'Szaluna Zębice'),
    ('Burza Chwalibożyce', 'Odra Kotowice'), ('Zorza Niemil', 'Jankowianka Wierzbno'),
    ('Polonia Godzikowice', 'Czarni Sobocisko'), ('Orzeł Święta Katarzyna', 'Sokół II Marcinkowice'),
    # Kolejka 21
    ('Burza Chwalibożyce', 'Jankowianka Wierzbno'), ('Orzeł Święta Katarzyna', 'MKS Siechnice'),
    ('Sokół II Marcinkowice', 'Polonia Godzikowice'), ('Czarni Sobocisko', 'Zorza Niemil'),
    ('Odra Kotowice', 'Lotos Gaj Oławski'), ('Szaluna Zębice', 'Moto Jelcz II Oława'),
    # Kolejka 22
    ('MKS Siechnice', 'Szaluna Zębice'), ('Moto Jelcz II Oława', 'Odra Kotowice'),
    ('Lotos Gaj Oławski', 'Jankowianka Wierzbno'), ('Burza Chwalibożyce', 'Czarni Sobocisko'),
    ('Zorza Niemil', 'Sokół II Marcinkowice'), ('Polonia Godzikowice', 'Orzeł Święta Katarzyna')
]


def simulate_match(home, away):
    # Model Poissona (bonus 14% dla gospodarza wg. statystyk z 1 polowy sezonu)
    h_lambda = current_stats[home]['att'] * current_stats[away]['def'] * 1.07 / 2.0
    a_lambda = current_stats[away]['att'] * current_stats[home]['def'] * 0.93/ 2.0
    h_goals = np.random.poisson(h_lambda)
    a_goals = np.random.poisson(a_lambda)
    if h_goals > a_goals:
        return 3, 0
    elif h_goals < a_goals:
        return 0, 3
    else:
        return 1, 1

# 3. SYMULACJA
iterations = 10000
results = defaultdict(lambda: defaultdict(int))
total_points_accumulated = defaultdict(int)

for _ in range(iterations):
    season_pts = {t: d['pts'] for t, d in current_stats.items()}
    for h, a in fixtures:
        hp, ap = simulate_match(h, a)
        season_pts[h] += hp
        season_pts[a] += ap

    sorted_teams = sorted(season_pts.items(), key=lambda x: x[1], reverse=True)
    for rank, (team, pts) in enumerate(sorted_teams, 1):
        results[team][rank] += 1
        total_points_accumulated[team] += pts

summary_data = []
for team in sorted(current_stats.keys()):
    win_pct = (results[team][1] / iterations) * 100
    second_pct = (results[team][2] / iterations) * 100
    top3_pct = ((results[team][1] + results[team][2] + results[team][3]) / iterations) * 100
    avg_pos = sum(r * c for r, c in results[team].items()) / iterations
    avg_pts = total_points_accumulated[team] / iterations

    summary_data.append({
        'Drużyna': team,
        'Śr. pkt': round(avg_pts, 1),
        '1. msc (%)': f"{win_pct:.2f}%",
        '2. msc (%)': f"{second_pct:.2f}%",
        'TOP 3 (%)': f"{top3_pct:.2f}%",
        'Śr. pozycja': round(avg_pos, 2)
    })

df_summary = pd.DataFrame(summary_data).sort_values('Śr. pkt')
print(df_summary.to_string(index=False))