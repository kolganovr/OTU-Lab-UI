import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt



class Solver:
        def __init__(self, equation_function, initial_conditions, t_span):
            self.equation_function = equation_function
            self.initial_conditions = initial_conditions
            self.t_span = t_span

        def solve(self):
            solution = solve_ivp(self.equation_function, self.t_span, self.initial_conditions,
                                 method='RK45',
                                 # Параметр, определяющий моменты времени (100 точек),
                                 # в которые будет выполняться интерполяция результата
                                 t_eval=np.linspace(self.t_span[0], self.t_span[1], 100))
            return solution

class UserInterface:
    def get_input(self):
        pass

    def display_output():
        pass
