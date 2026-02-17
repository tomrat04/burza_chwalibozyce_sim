import numpy as np
import pandas as pd
from collections import defaultdict
import random
import matplotlib.pyplot as plt
from scipy.stats import poisson

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

home_stats = {
    'MKS Siechnice': {'att': 5.40, 'def': 3.40},
    'Polonia Godzikowice': {'att': 1.50, 'def': 3.67},
    'Orzeł Święta Katarzyna': {'att': 2.80, 'def': 2.20},
    'Zorza Niemil': {'att': 1.67, 'def': 2.67},
    'Sokół II Marcinkowice': {'att': 4.40, 'def': 1.60},
    'Burza Chwalibożyce': {'att': 4.50, 'def': 2.75},
    'Czarni Sobocisko': {'att': 4.75, 'def': 1.75},
    'Lotos Gaj Oławski': {'att': 2.33, 'def': 2.67},
    'Jankowianka Wierzbno': {'att': 2.33, 'def': 5.17},
    'Moto Jelcz II Oława': {'att': 6.83, 'def': 1.83},
    'Odra Kotowice': {'att': 1.67, 'def': 2.17},
    'Szaluna Zębice': {'att': 2.00, 'def': 3.29}
}

away_stats = {
    'MKS Siechnice': {'att': 4.83, 'def': 0.50},
    'Polonia Godzikowice': {'att': 0.80, 'def': 6.40},
    'Orzeł Święta Katarzyna': {'att': 3.33, 'def': 4.83},
    'Zorza Niemil': {'att': 2.00, 'def': 2.40},
    'Sokół II Marcinkowice': {'att': 2.83, 'def': 3.83},
    'Burza Chwalibożyce': {'att': 3.57, 'def': 3.43},
    'Czarni Sobocisko': {'att': 4.43, 'def': 1.57},
    'Lotos Gaj Oławski': {'att': 2.60, 'def': 3.20},
    'Jankowianka Wierzbno': {'att': 0.80, 'def': 3.80},
    'Moto Jelcz II Oława': {'att': 2.00, 'def': 2.40},
    'Odra Kotowice': {'att': 1.00, 'def': 3.00},
    'Szaluna Zębice': {'att': 4.5, 'def': 4.00}
}

fixtures = [
    ('MKS Siechnice', 'Polonia Godzikowice'), ('Orzeł Święta Katarzyna', 'Zorza Niemil'),
    ('Sokół II Marcinkowice', 'Burza Chwalibożyce'), ('Czarni Sobocisko', 'Lotos Gaj Oławski'),
    ('Jankowianka Wierzbno', 'Moto Jelcz II Oława'), ('Odra Kotowice', 'Szaluna Zębice'),
    ('Odra Kotowice', 'MKS Siechnice'), ('Szaluna Zębice', 'Jankowianka Wierzbno'),
    ('Moto Jelcz II Oława', 'Czarni Sobocisko'), ('Lotos Gaj Oławski', 'Sokół II Marcinkowice'),
    ('Burza Chwalibożyce', 'Orzeł Święta Katarzyna'), ('Zorza Niemil', 'Polonia Godzikowice'),
    ('MKS Siechnice', 'Zorza Niemil'), ('Polonia Godzikowice', 'Burza Chwalibożyce'),
    ('Orzeł Święta Katarzyna', 'Lotos Gaj Oławski'), ('Sokół II Marcinkowice', 'Moto Jelcz II Oława'),
    ('Czarni Sobocisko', 'Szaluna Zębice'), ('Jankowianka Wierzbno', 'Odra Kotowice'),
    ('Czarni Sobocisko', 'Odra Kotowice'), ('Jankowianka Wierzbno', 'MKS Siechnice'),
    ('Szaluna Zębice', 'Sokół II Marcinkowice'), ('Moto Jelcz II Oława', 'Orzeł Święta Katarzyna'),
    ('Lotos Gaj Oławski', 'Polonia Godzikowice'), ('Burza Chwalibożyce', 'Zorza Niemil'),
    ('MKS Siechnice', 'Burza Chwalibożyce'), ('Zorza Niemil', 'Lotos Gaj Oławski'),
    ('Polonia Godzikowice', 'Moto Jelcz II Oława'), ('Orzeł Święta Katarzyna', 'Szaluna Zębice'),
    ('Sokół II Marcinkowice', 'Odra Kotowice'), ('Czarni Sobocisko', 'Jankowianka Wierzbno'),
    ('Czarni Sobocisko', 'MKS Siechnice'), ('Jankowianka Wierzbno', 'Sokół II Marcinkowice'),
    ('Odra Kotowice', 'Orzeł Święta Katarzyna'), ('Szaluna Zębice', 'Polonia Godzikowice'),
    ('Moto Jelcz II Oława', 'Zorza Niemil'), ('Lotos Gaj Oławski', 'Burza Chwalibożyce'),
    ('MKS Siechnice', 'Lotos Gaj Oławski'), ('Burza Chwalibożyce', 'Moto Jelcz II Oława'),
    ('Zorza Niemil', 'Szaluna Zębice'), ('Polonia Godzikowice', 'Odra Kotowice'),
    ('Orzeł Święta Katarzyna', 'Jankowianka Wierzbno'), ('Sokół II Marcinkowice', 'Czarni Sobocisko'),
    ('Burza Chwalibożyce', 'Szaluna Zębice'), ('Sokół II Marcinkowice', 'MKS Siechnice'),
    ('Czarni Sobocisko', 'Orzeł Święta Katarzyna'), ('Jankowianka Wierzbno', 'Polonia Godzikowice'),
    ('Odra Kotowice', 'Zorza Niemil'), ('Moto Jelcz II Oława', 'Lotos Gaj Oławski'),
    ('MKS Siechnice', 'Moto Jelcz II Oława'), ('Lotos Gaj Oławski', 'Szaluna Zębice'),
    ('Burza Chwalibożyce', 'Odra Kotowice'), ('Zorza Niemil', 'Jankowianka Wierzbno'),
    ('Polonia Godzikowice', 'Czarni Sobocisko'), ('Orzeł Święta Katarzyna', 'Sokół II Marcinkowice'),
    ('Burza Chwalibożyce', 'Jankowianka Wierzbno'), ('Orzeł Święta Katarzyna', 'MKS Siechnice'),
    ('Sokół II Marcinkowice', 'Polonia Godzikowice'), ('Czarni Sobocisko', 'Zorza Niemil'),
    ('Odra Kotowice', 'Lotos Gaj Oławski'), ('Szaluna Zębice', 'Moto Jelcz II Oława'),
    ('MKS Siechnice', 'Szaluna Zębice'), ('Moto Jelcz II Oława', 'Odra Kotowice'),
    ('Lotos Gaj Oławski', 'Jankowianka Wierzbno'), ('Burza Chwalibożyce', 'Czarni Sobocisko'),
    ('Zorza Niemil', 'Sokół II Marcinkowice'), ('Polonia Godzikowice', 'Orzeł Święta Katarzyna')
]

def get_weighted_stat(team, stat_type, context):
    weight_specific = 0.3 # waga statystyk dom/wyjazd
    weight_general = 0.7 # waga statystyk ogólnych

    if context == 'home':
        specific_val = home_stats[team][stat_type]
    else:
        specific_val = away_stats[team][stat_type]

    general_val = current_stats[team][stat_type]

    return (specific_val * weight_specific) + (general_val * weight_general)


def simulate_match(home, away):
    h_att = get_weighted_stat(home, 'att', 'home')
    h_def = get_weighted_stat(home, 'def', 'home')
    a_att = get_weighted_stat(away, 'att', 'away')
    a_def = get_weighted_stat(away, 'def', 'away')

    home_perf = random.uniform(0.75, 1.25)
    away_perf = random.uniform(0.75, 1.25)


    home_advantage = 1.1

    h_lambda = ((h_att + a_def)* home_advantage / 2.0) * home_perf
    a_lambda = ((a_att + h_def) / 2.0) * away_perf

    h_goals = np.random.poisson(h_lambda)
    a_goals = np.random.poisson(a_lambda)

    return h_goals, a_goals

iterations = 100000
results = defaultdict(lambda: defaultdict(int))
total_points_accumulated = defaultdict(int)

def poisson_charts():
    names = list(current_stats.keys())

    # Oś X (gole od 0 do 10)
    x = np.arange(0, 11)

    fig, axes = plt.subplots(6, 2, figsize=(12, 18))
    axes = axes.flatten()
    for i in range(len(names)):
        ax = axes[i]
        team = names[i]

        att = current_stats[team]['att']
        def_ = current_stats[team]['def']

        ax.plot(x, poisson.pmf(x, att), 'g-', label=f'scored goals distribution ({att})')
        ax.plot(x, poisson.pmf(x, def_), 'r-', label=f'lost goals distribution ({def_})')

        ax.set_title(team)
        ax.legend()

    plt.tight_layout()
    plt.savefig('img/distributions.jpg')
    plt.show()

poisson_charts()

for i in range(iterations):
    if i%100==0:
        print(f'completed in {i/iterations*100: .1f}%\n-------------------')
    season_pts = {t: d['pts'] for t, d in current_stats.items()}

    for h, a in fixtures:
        hg, ag = simulate_match(h, a)

        if hg > ag:
            season_pts[h] += 3
        elif ag > hg:
            season_pts[a] += 3
        else:
            season_pts[h] += 1
            season_pts[a] += 1

    sorted_teams = sorted(season_pts.items(), key=lambda x: (x[1], random.random()), reverse=True)

    for rank, (team, pts) in enumerate(sorted_teams, 1):
        results[team][rank] += 1
        total_points_accumulated[team] += pts

summary_data = []
for team in sorted(current_stats.keys()):
    win = (results[team][1] / iterations) * 100
    top2 = ((results[team][1] + results[team][2]) / iterations) * 100
    top3 = ((results[team][1] + results[team][2] + results[team][3]) / iterations) * 100
    avg_pos = sum(r * c for r, c in results[team].items()) / iterations
    avg_pts = total_points_accumulated[team] / iterations

    summary_data.append({
        'Drużyna': team,
        'Śr. pkt': round(avg_pts, 1),
        '1 miejsce (%)': f"{win:.2f}%",
        'TOP 2 (%)': f"{top2:.2f}%",
        'TOP 3 (%)': f"{top3:.2f}%",
        'Śr. pozycja': round(avg_pos, 1)
    })

df_summary = pd.DataFrame(summary_data).sort_values('Śr. pozycja', ascending=True)

print(df_summary.to_string(index=False))

df_summary.to_excel('symulacja.xlsx', index=False)
print("Zapisano wyniki do pliku 'symulacja.xlsx'")