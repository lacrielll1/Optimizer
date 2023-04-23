def hu_tao_atk(stats):
    # Hu Tao lv 90 base = 106.43
    # Homa lv 90 base = 608.07
    # Hu Tao lv 90 base hp = 15552
    # Homa + 20% hp, + 1.8% atk by hp in sum. 6.26% by talent
    return ((106.43 + 608.07) * (1 + stats['atk%'] / 100) + stats['flat_atk'] +
      (15552 * (1 + stats['hp%'] / 100 + 20 / 100) + stats['flat_hp']) * (6.26 + 1.8) / 100)
    
def get_base_dmg(atk, mv):
    return atk * mv / 100

def get_def_mult(lc, le, dr, di):
    return (lc + 100) / (lc + 100 + (le + 100) * (1-dr / 100) * (1-di / 100))

def get_res_mult(br, red):
    res = (br - red) / 100
    if res < 0:
        return 1 - res / 2
    elif res >= 0 and res < 0.75:
        return 1 - res
    return 1 / (4 * res + 1)
    
def get_amplifying_reaction(mul, em, rb):
    return mul * (1 + (2.78 * em) / (1400 + em) + rb / 100)

def hu_tao_9n1cd_q_homa_vape(stats):
    return (get_base_dmg(hu_tao_atk(stats), stats['mv_combo']) * 
            (1 + stats['dmg_bonus%'] / 100) * (1 + min(100, stats['cr']) * stats['cd'] / 10000) *
              get_def_mult(90, 90, stats['def_red'], stats['def_ignore']) * get_res_mult(10, stats['res_red']) *
                get_amplifying_reaction(1.5, stats['em'], stats['reaction_bonus']))

    