import numpy as np
from itertools import product
import copy
from scipy.optimize import NonlinearConstraint
from scipy.optimize import Bounds
from scipy.optimize import minimize
from objective import *

from artifact import BaseArtifact
from constraints import *


stats = ['flat_hp', 'flat_atk', 'em', 'cr', 'cd', 'hp%', 'atk%', 'er%', 'flat_def', 'def%']

rolls = {
    'flat_hp': np.linspace(209.13, 298.75, 4),
    'flat_atk': np.linspace(13.62, 19.45, 4),
    'flat_def': np.linspace(16.2, 23.15, 4),
    'hp%': np.linspace(4.08, 5.83, 4),
    'atk%': np.linspace(4.08, 5.83, 4),
    'def%': np.linspace(5.10, 7.29, 4),
    'em': np.linspace(16.32, 23.31, 4),
    'er%': np.linspace(4.53, 6.48, 4),
    'cr': np.linspace(2.72, 3.89, 4),
    'cd': np.linspace(5.44, 7.77, 4),
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
    'hp%': 46.6, 'def%': 58.3, 'cr': 31.1, 'atk%': 46.6, 'em': 186.5, 'cd': 62.2, 'hb': 35.9,
}

# Ограничения в удобном виде
constraints = {
    'sum': [constraint_rolls_sum, 35, 40],
    'flat_hp': [constraint_flat_hp, 1, 30],
    'flat_atk': [constraint_flat_atk, 1, 30],
    'em': [constraint_em, 1, 30],
    'cr': [constraint_cr, 1, 30],
    'cd': [constraint_cd, 1, 30],
    'hp%': [constraint_hp, 1, 30],
    'atk%': [constraint_atk, 1, 30],
    'er%': [constraint_er, 1, 30],
    'flat_def': [constraint_flat_def, 1, 30],
    'def%': [constraint_def, 1, 30],
}

def get_base_artifacts(main_stats):
    return [BaseArtifact(k, v) for k, v in main_stats.items()]

def get_stats(x: list, subs: list, arts: tuple[BaseArtifact], buffs: dict, base_stats: dict):
    st = {subs[i]: x[4 * i: 4 * i + 4] for i in range(len(subs))}
    stat_values = {}
    stat_values['hb'] = 0
    stat_values['dmg_bonus%'] = 0
    for k, v in st.items():
        stat_values[k] = sum([x * y for x, y in zip(v, rolls[k])])
    for art in arts:
        stat_values[art.main_stat] += art.main_stat_value
    for k, v in buffs.items():
        if k not in list(stat_values.keys()):
            stat_values[k] = v
        else:
            stat_values[k] += v
    for k, v in base_stats.items():
        if k not in list(stat_values.keys()):
            stat_values[k] = v
        else:
            stat_values[k] += v
    return stat_values

def make_constraints(constraints_dict):
    return [NonlinearConstraint(v[0], v[1], v[2]) for k, v in constraints_dict.items()]

def wrapper(x, subs, arts, buffs, base_stats, obj):
    return -obj(get_stats(x, subs, arts, buffs, base_stats))

def optimize_obj(buffs, base_stats, obj):
    flowers = get_base_artifacts(flower_main_values)
    plumes = get_base_artifacts(plume_main_values)
    sands = get_base_artifacts(sands_main_values)
    goblets = get_base_artifacts(goblet_main_values)
    heads = get_base_artifacts(head_main_values)
    all_combs = list(product(flowers, plumes, sands, goblets, heads)) # 210 вариантов
    max_dmg = 0
    best_rolls = None
    best_comb = None
    for comb in all_combs:
        x = list([0.9]) * 40
        lb = list([0.001]) * 40
        ub = list([40.0000001]) * 40
        bnd = Bounds(lb, ub)
        tmp_constr = copy.deepcopy(constraints)
        main_stats = [art.main_stat for art in comb]
        counts = {k: main_stats.count(k) for k in main_stats}
        for k, v in counts.items():
            if k == 'hb' or k == 'dmg_bonus%':
                continue
            tmp_constr[k][2] -= v * 6
        constr = make_constraints(tmp_constr)
        res = minimize(wrapper, x, (stats, comb, buffs, base_stats, obj), 'trust-constr', constraints=constr,
                        bounds=bnd)
        if -res.fun > max_dmg:
            max_dmg = -res.fun
            best_rolls = res.x
            best_comb = comb
    return best_rolls, best_comb, max_dmg

objs = [hu_tao_9n1cd_q_homa_vape]
buffs = [{
        'em': 200 + 120 + 100, # с2 Казах + элегия + инструктор
        'res_red': 40,
        'atk%': 20,
        'dmg_bonus%': 40,
    }, {}]
for buff in buffs:
    for obj in objs:
        base_stats = {
            'mv_combo': 83.65 * 9 + 242.56 * 9 + 617.44, # ротация
            'dmg_bonus%': 33 + 15 + 15 / 2, # сет ведьмы + 1 стак + < 50% хп пассивка
            'cr': 5,
            'cd': 50 + 38.4 + 66.15, # прокачка при уровне + хома
            'er%': 100,
            'def_red': 0,
            'def_ignore': 0,
            'res_red': 0,
            'reaction_bonus': 15,
            'em': 0,
            'hp%': 0,
            'atk%': 0,
            'def%': 0
        }
        
        best_rolls, best_comb, max_dmg = optimize_obj(buff, base_stats, obj)
        r = {}
        best_rolls = np.round(best_rolls).astype(np.int32)
        for i in range(len(stats)):
            r[stats[i]] = best_rolls[4 * i: 4 * i + 4]
        stats_ = get_stats(best_rolls, stats, best_comb, buff, base_stats)
        print(r)
        [print(art.main_stat) for art in best_comb]
        print(stats_)
        print(max_dmg)
        print(15552 * (stats_['hp%'] + 20) / 100 + stats_['flat_hp'])




