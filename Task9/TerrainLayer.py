from FractalTerrain import FractalTerrain


class TerrainLayer:
    def __init__(self, start_x, start_y, end_x, end_y, roughness, iterations, color='black'):
        self.terrain = FractalTerrain(start_x, start_y, end_x, end_y, roughness, iterations)
        self.points = []
        self.color = color
        self.canvas_elements = []

    def generate(self):
        self.points = self.terrain.generate()
        return self.points

    def get_points_as_arrays(self):
        return self.terrain.get_points_as_arrays()
