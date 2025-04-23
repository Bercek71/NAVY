class FractalAppConfig:

    # base konfigurace
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 800
    DEFAULT_MAX_ITER = 100
    DEFAULT_COLORSCALE = 'Viridis'

    # podporované barevné škály
    COLORSCALES = ['Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis', 'Turbo',
                   'Hot', 'Jet', 'Rainbow', 'Bluered', 'Electric']

    # výchozí pohledy podle zadání
    DEFAULT_MANDELBROT_VIEW = {'x_min': -2.0, 'x_max': 1.0, 'y_min': -1.0, 'y_max': 1.0}
    DEFAULT_JULIA_VIEW = {'x_min': -1.5, 'x_max': 1.5, 'y_min': -1.5, 'y_max': 1.5}
