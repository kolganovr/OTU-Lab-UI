from numpy import linspace
from scipy.integrate import solve_ivp
# Класс инициализирующий все параметры конечного уравнения
class LastEquation(object):
    def __init__(self, n: int):
        self.n = n
        self.a_0 = 0
        self.a_1 = 0
        self.a_2 = 0
        self.a_3 = 0
        self.b_0 = 0

    def init_order_2(self, a_0: float, a_1: float, a_2: float, b_0: float):
        self.a_0 = a_0
        self.a_1 = a_1
        self.a_2 = a_2
        self.b_0 = b_0

    def init_order_3(self, a_0: float, a_1: float, a_2: float, a_3: float, b_0: float):
        self.a_0 = a_0
        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3
        self.b_0 = b_0

    def show_inf(self):
        print(self.n, self.a_0, self.a_1, self.a_2, self.a_3, self.b_0)

# Класс для решения системы уравнений
class Solver:
        def __init__(self, equation_function, initial_conditions, t_span, y, last_equation):
            self.equation_function = equation_function
            self.initial_conditions = initial_conditions
            self.t_span = t_span
            self.y = y
            self.last_equation = last_equation

        def solve(self):
            solution = solve_ivp(self.equation_function, self.t_span, self.initial_conditions,
                                 method='RK45',
                                 # Параметр, определяющий моменты времени (100 точек),
                                 # в которые будет выполняться интерполяция результата
                                 t_eval=linspace(self.t_span[0], self.t_span[1], 300), args=(self.y, self.last_equation))
            return solution
