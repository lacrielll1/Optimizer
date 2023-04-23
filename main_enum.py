import numpy as np
import itertools
from itertools import product

from artifact import Artifact

stats_ = ['flat_hp', 'flat_atk', 'em', 'cr', 'cd', 'hp%', 'atk%', 'er%', 'flat_def', 'def%']
#stats_ = ['flat_hp', 'em', 'cr', 'cd', 'hp%']

main_stats = ['hp%', 'def%', 'er%', 'atk%', 'em']
ignore = ['er%', 'def%', 'atk%', 'hb']
rolls = {
    'flat_hp': np.linspace(209.13, 298.75, 4)[2],
    'flat_atk': np.linspace(13.62, 19.45, 4)[2],
    'flat_def': np.linspace(16.2, 23.15, 4)[2],
    'hp%': np.linspace(4.08, 5.83, 4)[2],
    'atk%': np.linspace(4.08, 5.83, 4)[2],
    'def%': np.linspace(5.10, 7.29, 4)[2],
    'em': np.linspace(16.32, 23.31, 4)[2],
    'er%': np.linspace(4.53, 6.48, 4)[2],
    'cr': np.linspace(2.72, 3.89, 4)[2],
    'cd': np.linspace(5.44, 7.77, 4)[2],
}

flower_main_values = {
    'flat_hp': 4780
}

plume_main_values = {
    'flat_atk': 311
}

sands_main_values = {
    'hp%': 46.6, 'def%': 58.3, 'er%': 51.8, 'atk%': 46.6, 'em': 186.5,
}

goblet_main_values = {
    'hp%': 46.6, 'def%': 58.3, 'dmg_bonus%': 46.6, 'atk%': 46.6, 'em': 186.5,
}

head_main_values = {
    'hp%': 46.6, 'def%': 58.3, 'cr%': 31.1, 'atk%': 46.6, 'em': 186.5, 'cd': 62.2, 'hb': 35.9,
}


def get_stats_comb():
    elements = list(range(6))
    # Генерируем все возможные комбинации с повторением элементов
    combinations = list(itertools.combinations_with_replacement(elements, 4))
    # Отбираем только валидные комбинации
    valid_combinations_four = [c for c in combinations 
                        if c[0] <= 6 and c[1] <= 6 and c[2] <= 6 and c[3] <= 6 and c[0] >= 1 and c[1] >= 1 and c[2] >= 1 and c[3] >= 1
                        and sum(c) == 9]
    valid_combinations_three = [c for c in combinations 
                        if c[0] <= 5 and c[1] <= 5 and c[2] <= 5 and c[3] <= 5 and c[0] >= 1 and c[1] >= 1 and c[2] >= 1 and c[3] >= 1
                        and sum(c) == 8]
    valid = []
    valid.extend(valid_combinations_four)
    valid.extend(valid_combinations_three)
    subs_comb = list(set(sorted(list(itertools.combinations(stats_, 4)))))
    return subs_comb, valid


def get_artifacts(main_values: dict):
    subs_comb, valid = get_stats_comb()
    artifacts = [
        Artifact({k: v}, {key: value * rolls[key] for key, value in zip(stats, val)})
        for k, v in main_values.items()
        if k not in valid and k not in ignore
        for stats in subs_comb
        for val in valid
    ]
    return artifacts

flowers = get_artifacts(flower_main_values)
plumes = get_artifacts(plume_main_values)
sands = get_artifacts(sands_main_values)
goblets = get_artifacts(goblet_main_values)
heads = get_artifacts(head_main_values)

print(len(flowers) * len(plumes) * len(goblets) * len(heads) * len(sands))

# cartesian_product = list(product(flowers, plumes, sands, goblets, heads))
# print(len(cartesian_product))









