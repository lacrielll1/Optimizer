# Ограничение на количество роллов от 35 до 40 на +20 артах
def constraint_rolls_sum(x):
    return sum(x)

def constraint_flat_hp(x):
    return sum(x[0:4])

def constraint_flat_atk(x):
    return sum(x[4:8])

def constraint_em(x):
    return sum(x[8:12])

def constraint_cr(x):
    return sum(x[12:16])

def constraint_cd(x):
    return sum(x[16:20])

def constraint_hp(x):
    return sum(x[20:24])

def constraint_atk(x):
    return sum(x[24:28])

def constraint_er(x):
    return sum(x[28:32])

def constraint_flat_def(x):
    return sum(x[32:36])

def constraint_def(x):
    return sum(x[36:40])