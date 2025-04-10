class AffineTransformation:

    def __init__(self, coefficients, probability = 0.25):

        if len(coefficients) != 12:
            raise ValueError("Affine transformation requires exactly 12 coefficients")

        self.coefficients = coefficients
        self.probability = probability

    # provedení transformace
    def apply(self, point):

        x, y, z = point
        a, b, c, d, e, f, g, h, i, j, k, l = self.coefficients

        # písmenková polívka
        x_new = a * x + b * y + c * z + j
        y_new = d * x + e * y + f * z + k
        z_new = g * x + h * y + i * z + l

        return x_new, y_new, z_new
