import numpy as np


class LogisticMap:
    def __init__(self):
        pass

    def compute(self, x, a):
        return a * x * (1 - x)

    def generate_data(self, a_min=2.8, a_max=4.0, n_a=300, n_iterations=200, n_skip=100):
        print(f"Generating bifurcation data with {n_a} parameter values...")

        a_values = np.linspace(a_min, a_max, n_a)
        x_values = []

        for a in a_values:
            x = 0.5

            for _ in range(n_skip):
                x = self.compute(x, a)

            attractor_points = []
            for _ in range(n_iterations - n_skip):
                x = self.compute(x, a)
                attractor_points.append(x)

            x_values.append(attractor_points)

        return a_values, x_values
