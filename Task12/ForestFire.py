import random

import numpy as np


class ForestFire:
    EMPTY = 0
    TREE = 1
    BURNING = 2
    BURNT = 3

    COLORS = {
        EMPTY: '#8B4513', #  brown
        TREE: '#228B22', # green
        BURNING: '#FF4500', # red
        BURNT: '#A9A9A9' #gray
    }

    def __init__(self, size=100, p=0.05, f=0.001, density=0.5, use_moore=False):
        self.size = size # velikost gridu
        self.p = p # pravdepodobnost, ze se na prazdnem miste objevi strom
        self.f = f # pravdepodobnost, ze se na miste se stromem objevi ohen
        self.density = density
        self.use_moore = use_moore
        self.grid = self._initialize_grid()

    def _initialize_grid(self):
        grid = np.zeros((self.size, self.size), dtype=int)

        for i in range(self.size):
            for j in range(self.size):
                if random.random() < self.density:
                    grid[i, j] = self.TREE


        # nahodny pocet stromu, ktery bude hořet na zacatku
        burning_count = max(1, int(0.001 * self.size * self.size))
        for _ in range(burning_count):
            i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if grid[i, j] == self.TREE:
                grid[i, j] = self.BURNING

        return grid

    def _get_neighbors(self, i, j):
        neighbors = []

        if not self.use_moore:
            # muze jit jenom nahoru, dolu, vlevo, vpravo
            directions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        else:
            # muze jit i do diagonaly
            directions = [
                (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1),
                (i + 1, j), (i + 1, j - 1), (i, j - 1), (i - 1, j - 1)
            ]

        return [(x, y) for x, y in directions if 0 <= x < self.size and 0 <= y < self.size]

    def update(self):
        new_grid = self.grid.copy()

        for i in range(self.size):
            for j in range(self.size):
                state = self.grid[i, j]

                if state == self.EMPTY or state == self.BURNT:
                    if random.random() < self.p:
                        new_grid[i, j] = self.TREE
                    else:
                        new_grid[i, j] = state

                elif state == self.TREE:
                    neighbors = self._get_neighbors(i, j)
                    neighbor_burning = any(self.grid[x, y] == self.BURNING for x, y in neighbors)

                    if neighbor_burning:
                        new_grid[i, j] = self.BURNING
                    elif random.random() < self.f:
                        new_grid[i, j] = self.BURNING

                elif state == self.BURNING:
                    new_grid[i, j] = self.BURNT

        self.grid = new_grid
        return self.grid

    def reset(self, p=None, f=None, use_moore=None):
        if p is not None:
            self.p = p
        if f is not None:
            self.f = f
        if use_moore is not None:
            self.use_moore = use_moore

        self.grid = self._initialize_grid()
        return self.grid

    @property
    def color_scale(self):
        return [self.COLORS[self.EMPTY], self.COLORS[self.TREE],
                self.COLORS[self.BURNING], self.COLORS[self.BURNT]]
