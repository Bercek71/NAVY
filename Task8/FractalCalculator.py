import numpy as np


class FractalCalculator:

    @staticmethod
    def compute_mandelbrot(width, height, max_iter, x_min=-2.0, x_max=1.0, y_min=-1.0, y_max=1.0):
        # vytoření komplexního prostoru
        re = np.linspace(x_min, x_max, width)
        im = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(re, im)
        c = X + 1j * Y

        # inicializace
        z = np.zeros_like(c)
        iterations = np.zeros(c.shape, dtype=int)
        mask = np.ones(c.shape, dtype=bool)

        # iterování a ohlídání bodů které utíkají
        for i in range(max_iter):
            # spočítání mandelbrot funkce
            z[mask] = z[mask] ** 2 + c[mask]
            # pokud je bod mimo jednotkovou kružnici, zapíšeme iteraci
            escaped = np.abs(z) > 2.0
            # pokud bod unikl, zapíšeme iteraci
            iterations[mask & escaped] = i
            # maska pro body které unikly
            mask[escaped] = False


            if not np.any(mask):
                break

        return iterations

    @staticmethod
    def compute_julia(width, height, c, max_iter, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
        re = np.linspace(x_min, x_max, width)
        im = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(re, im)
        z = X + 1j * Y

        iterations = np.zeros(z.shape, dtype=int)
        mask = np.ones(z.shape, dtype=bool)

        for i in range(max_iter):
            # obdobně jako u mandelbrot, akorát funkce je jiná a c je konstantní
            z[mask] = z[mask] ** 2 + c
            escaped = np.abs(z) > 2.0
            iterations[mask & escaped] = i
            mask[escaped] = False

            if not np.any(mask):
                break

        return iterations
