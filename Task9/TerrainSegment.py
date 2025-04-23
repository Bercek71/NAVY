import math

from TerrainPoint import TerrainPoint


class TerrainSegment:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_midpoint(self):
        mid_x = (self.start.x + self.end.x) / 2
        mid_y = (self.start.y + self.end.y) / 2
        return TerrainPoint(mid_x, mid_y)

    def get_length(self):
        return math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)

    def __str__(self):
        return f"Segment from {self.start} to {self.end}"
