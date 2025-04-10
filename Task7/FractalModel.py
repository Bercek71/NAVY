import numpy as np

class FractalModel:

    def __init__(self, transformations, name = "Fractal Model"):
        self.transformations = transformations
        self.name = name
        self.probabilities = [t.probability for t in transformations]
        prob_sum = sum(self.probabilities)
        if prob_sum != 1.0:
            self.probabilities = [p / prob_sum for p in self.probabilities]

        # historie
        self.point_history = []
        self.current_point = (0, 0, 0)
        self.transformation_history = []

    def reset_history(self, initial_point = (0, 0, 0)):

        self.point_history = [initial_point]
        self.current_point = initial_point
        self.transformation_history = []

    def generate_next_point(self):

        # náhodný výběr transformace podle pravděpodobnosti
        transform_idx = np.random.choice(len(self.transformations), p=self.probabilities)

        # aplikace transformace
        self.current_point = self.transformations[transform_idx].apply(self.current_point)

        # přidání bodu do historie
        self.point_history.append(self.current_point)
        self.transformation_history.append(transform_idx)

        return self.current_point

    def generate_points(self, num_points = 10000,
                        initial_point = (0, 0, 0),
                        reset = True):

        if reset:
            self.reset_history(initial_point)


        # generování
        for _ in range(num_points):
            self.generate_next_point()

        # rozbalení pro snadnější manipulaci
        return self.get_history_arrays()

    def get_history_arrays(self):
        if not self.point_history:
            return np.array([]), np.array([]), np.array([])

        x_coords, y_coords, z_coords = zip(*self.point_history)
        return np.array(x_coords), np.array(y_coords), np.array(z_coords)

    def get_history_slice(self, start, end = None):

        if not self.point_history:
            return np.array([]), np.array([]), np.array([])

        history_slice = self.point_history[start:end]
        x_coords, y_coords, z_coords = zip(*history_slice)
        return np.array(x_coords), np.array(y_coords), np.array(z_coords)

    def get_stats(self) -> dict:
        if not self.transformation_history:
            return {"points": 0, "transformations": {}}

        transform_counts = {}
        for i in range(len(self.transformations)):
            count = self.transformation_history.count(i)
            transform_counts[f"Transform {i + 1}"] = {
                "count": count,
                "percentage": count / len(self.transformation_history) * 100
            }

        return {
            "points": len(self.point_history),
            "transformations": transform_counts
        }

