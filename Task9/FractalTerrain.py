import random

from TerrainSegment import TerrainSegment
from TerrainPoint import TerrainPoint


class FractalTerrain:

    def __init__(self, start_x, start_y, end_x, end_y, roughness=0.5, iterations=8):

        self.start_point = TerrainPoint(start_x, start_y)
        self.end_point = TerrainPoint(end_x, end_y)
        self.roughness = roughness
        self.iterations = iterations
        self.points = [self.start_point, self.end_point]
        self.y_range = abs(end_y - start_y) * 0.5

    def generate(self):
        initial_segment = TerrainSegment(self.start_point, self.end_point)
        segments = [initial_segment]

        for i in range(self.iterations):
            new_segments = []
            # spočítá se nový rozsah y pro aktuální iteraci

            # mocninou dosáhnu menšího rozsahu, takže
            # se postupně zmenšuje (čím víc iterací, tím menší rozsah) asi to není nezbytně nutné a dalo by se řešit jinak,
            # ale vypadá to cool
            current_range = self.y_range * (self.roughness ** i)

            for segment in segments:
                # prostřední bod úsečky
                midpoint = segment.get_midpoint()

                # 50/50 nahoru/dolů
                if random.random() < 0.5:
                    midpoint.y -= random.uniform(0, current_range)
                else:
                    midpoint.y += random.uniform(0, current_range)

                # přidání segmentu
                left_segment = TerrainSegment(segment.start, midpoint)
                right_segment = TerrainSegment(midpoint, segment.end)

                new_segments.append(left_segment)
                new_segments.append(right_segment)

                # přidání prostředního bodu do seznamu
                self.points.append(midpoint)

            # nahražení původních segmentů novými
            segments = new_segments

        # setřízení bodů podle x
        self.points.sort(key=lambda p: p.x)
        return self.points

    def get_points_as_arrays(self):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        return x_values, y_values