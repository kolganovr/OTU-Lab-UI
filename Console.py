from Equation import LastEquation
from Solve import Solver
import numpy as np




print("Введите порядок системы: - ")
n = int(input())
a_0, a_1, a_2, a_3, b_0, last_equation # Константы уравнения

def init_const_values(n):
    print("Введите a_0 - ")
    a_0 = float(input())

    print("Введите a_1 - ")
    a_1 = float(input())

    print("Введите a_2 - ")
    a_2 = float(input())

    if(n == 3):
        print("Введите a_0 - ")
        a_3 = float(input())

    print("Введите b_0 - ")
    b_0 = float(input())

    if(n == 3):
        last_equation = LastEquation(n, a_0, a_1, a_2, a_3, b_0, 0,0,0)
    else:
        last_equation = LastEquation(n, a_0, a_1, a_2,None, b_0, 0,0,0)



init_const_values(n)

# Функция для 2 порядка системы
def func_2(t, x, y, last_func : LastEquation):
    dxdt = np.zeros(2)
    dxdt[0] = x[1]
    dxdt[1] = (1 / last_func.a_2) * (last_func.b_0*y - last_func.a_1*x[1] - last_func.a_0*x[0])
    return dxdt

def func_3(t, x, y, last_func: LastEquation):
    dxdt = np.zeros(3)
    dxdt[0] = x[1]
    dxdt[1] = x[2]
    dxdt[2] = (1 / last_func.a_3) * (last_func.b_0*y - last_func.a_2*x[2] - last_func.a_1*x[1] - last_func.a_0*x[0])
    return dxdt

solver = Solver()
