class TerrainPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, TerrainPoint):
            return False
        return self.x == other.x and self.y == other.y
