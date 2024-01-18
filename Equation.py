# import numpy as np

# class SystemDiffEquations(object):

#     def __init__(self, n: int, a_0: float, a_1: float, a_2: float,
#                  a_3: float = None, b_0: float = None, derivative_0: float = None,
#                                   derivative_1: float = None, derivative_2: float = None):
#         if a_3 is not None:
#             # Установка начальных констант уравнения при 3 порядке производной входного сигнала
#             self.n = n
#             self.a_0 = a_0
#             self.a_1 = a_1
#             self.a_2 = a_2
#             self.a_3 = a_3
#             self.b_0 = b_0
#             # Установка начальньных условий
#             self.derivative_0 = derivative_0
#             self.derivative_1 = derivative_1
#             self.derivative_2 = derivative_2
#         else:
#             # Установка начальных констант уравнения при 2 порядке производной входного сигнала
#             self.n = n
#             self.a_0 = a_0
#             self.a_1 = a_1
#             self.a_2 = a_2
#             self.b_0 = b_0
#             # Установка начальных условий
#             self.derivative_0 = derivative_0
#             self.derivative_1 = derivative_1


#     def show_information(self):
#         print(f"n - {self.n}\n"+
#               f"a_0 - {self.a_0}\n"+
#               f"a_1 - {self.a_1}\n"+
#               f"a_2 - {self.a_2}\n"+
#               f"a_3 - {self.a_3}\n"+
#               f"b_0 - {self.b_0}\n")


# def main():
#     systemDiffEquations = SystemDiffEquations(2, 7, 3, 1,2,10)
#     systemDiffEquations.initialize_init_condition(1,2)
#     print(systemDiffEquations.derivative_0, systemDiffEquations.derivative_1, systemDiffEquations.derivative_2)


# if __name__ == "__main__":
#     main()

class LastEquation(object):
    def __init__(self, n: int, a_0: float, a_1: float, a_2: float,
                 a_3: float = None, b_0: float = None):
        if a_3 is not None:
            # Установка начальных констант уравнения при 3 порядке производной входного сигнала
            self.n = n
            self.a_0 = a_0
            self.a_1 = a_1
            self.a_2 = a_2
            self.a_3 = a_3
            self.b_0 = b_0
        else:
            # Установка начальных констант уравнения при 2 порядке производной входного сигнала
            self.n = n
            self.a_0 = a_0
            self.a_1 = a_1
            self.a_2 = a_2
            self.b_0 = b_0

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math
class DifferentialEquationSystem:
    def __init__(self, equation_function, initial_conditions, t_span, y, last_equation ):
        self.equation_function = equation_function
        self.initial_conditions = initial_conditions
        self.t_span = t_span
        self.y = y
        self.last_equation = last_equation

    def solve(self):
        solution = solve_ivp(self.equation_function, self.t_span, self.initial_conditions,method='RK45',
                             t_eval=np.linspace(self.t_span[0], self.t_span[1], 100), args=(self.y, self.last_equation))
        return solution

# Пример использования класса для решения системы дифференциальных уравнений
def example_equation(t, y):
    x = math.sin(t)
    dydt = np.zeros(2)
    dydt[0] = y[1]
    dydt[1] = (1 / 3) * (10*x - 3*y[1] - 7*y[0])
    return dydt

def func_3(t, x, y, last_func: LastEquation):
    dxdt = np.zeros(3)
    dxdt[0] = x[1]
    dxdt[1] = x[2]
    dxdt[2] = (1 / last_func.a_3) * (last_func.b_0*y - last_func.a_2*x[2] - last_func.a_1*x[1] - last_func.a_0*x[0])
    return dxdt


# y0 = [1, 1, 1]  # начальные условия
# t_span = [0, 200]  # интервал интегрирования

# last_equation = LastEquation(3, 9, 6, 3, 3, 12)
# system = DifferentialEquationSystem(func_3, y0, t_span, 1, last_equation)
# solution = system.solve()

# # Визуализация результатов
# plt.plot(solution.t, solution.y[0], label='x(t)')
# plt.plot(solution.t, solution.y[1], label="x'(t)")
# plt.plot(solution.t, solution.y[2], label="x''(t)")
# plt.xlabel('t')
# plt.ylabel('x')
# plt.legend()
# plt.show()
