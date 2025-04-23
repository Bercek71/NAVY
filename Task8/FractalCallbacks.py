import time

import numpy as np
from dash import Output, Input, State
from plotly import graph_objects as go

from Task8.FractalAppConfig import FractalAppConfig
from Task8.FractalCalculator import FractalCalculator


class FractalCallbacks:

    @staticmethod
    def register_callbacks(app):

        # Změna typu fraktálu
        @app.callback(
            Output('julia-params', 'style'),
            Input('fractal-type', 'value')
        )
        def toggle_julia_params(fractal_type):
            if fractal_type == 'julia':
                return {'display': 'block'}
            else:
                return {'display': 'none'}

        # Generování náhodného parametru Julie
        @app.callback(
            [Output('julia-real', 'value'),
             Output('julia-imag', 'value')],
            Input('random-julia', 'n_clicks'),
            prevent_initial_call=True
        )
        def update_julia_param(n_clicks):
            angle = np.random.uniform(0, 2 * np.pi)
            magnitude = np.random.uniform(0.3, 0.9)
            real = magnitude * np.cos(angle)
            imag = magnitude * np.sin(angle)
            return real, imag

        @app.callback(
            Output('view-state', 'data'),
            Input('reset-view', 'n_clicks'),
            State('view-state', 'data'),
            prevent_initial_call=True
        )
        def reset_view(n_clicks, current_view):
            # Reset na výchozí pohledy
            return {
                'mandelbrot': FractalAppConfig.DEFAULT_MANDELBROT_VIEW.copy(),
                'julia': FractalAppConfig.DEFAULT_JULIA_VIEW.copy()
            }

        # aktualizace grafu
        @app.callback(
            [Output('fractal-graph', 'figure'),
             Output('performance-info', 'children')],
            [Input('fractal-type', 'value'),
             Input('julia-real', 'value'),
             Input('julia-imag', 'value'),
             Input('max-iter-slider', 'value'),
             Input('resolution-slider', 'value'),
             Input('colorscale', 'value'),
             Input('reset-view', 'n_clicks'),
             Input('fractal-graph', 'relayoutData')],
            [State('view-state', 'data')]
        )
        def update_fractal(fractal_type, julia_real, julia_imag, max_iter, resolution,
                           colorscale, reset_clicks, relayout_data, view_state):
            start_time = time.time()

            current_view = view_state[fractal_type]
            x_min, x_max = current_view['x_min'], current_view['x_max']
            y_min, y_max = current_view['y_min'], current_view['y_max']

            # aktualizace pohledu podle akce uživatele
            if relayout_data and ('xaxis.range[0]' in relayout_data or 'xaxis.autorange' in relayout_data):
                if 'xaxis.autorange' in relayout_data and relayout_data['xaxis.autorange']:
                    if fractal_type == 'mandelbrot':
                        x_min, x_max = FractalAppConfig.DEFAULT_MANDELBROT_VIEW['x_min'], \
                        FractalAppConfig.DEFAULT_MANDELBROT_VIEW['x_max']
                        y_min, y_max = FractalAppConfig.DEFAULT_MANDELBROT_VIEW['y_min'], \
                        FractalAppConfig.DEFAULT_MANDELBROT_VIEW['y_max']
                    else:
                        x_min, x_max = FractalAppConfig.DEFAULT_JULIA_VIEW['x_min'], \
                        FractalAppConfig.DEFAULT_JULIA_VIEW['x_max']
                        y_min, y_max = FractalAppConfig.DEFAULT_JULIA_VIEW['y_min'], \
                        FractalAppConfig.DEFAULT_JULIA_VIEW['y_max']
                else:
                    # Získání nových hranic z akce přiblížení/posunutí
                    if all(k in relayout_data for k in
                           ['xaxis.range[0]', 'xaxis.range[1]', 'yaxis.range[0]', 'yaxis.range[1]']):
                        x_min = relayout_data['xaxis.range[0]']
                        x_max = relayout_data['xaxis.range[1]']
                        y_min = relayout_data['yaxis.range[0]']
                        y_max = relayout_data['yaxis.range[1]']

            # Úprava rozlišení podle poměru stran
            width = resolution
            height = int(width * abs(y_max - y_min) / abs(x_max - x_min))

            # výpočet fraktálu
            if fractal_type == 'mandelbrot':
                iterations = FractalCalculator.compute_mandelbrot(
                    width, height, max_iter, x_min, x_max, y_min, y_max
                )
                title = f"Mandelbrot set (Rozlišení: {width}x{height}, Max. iterací: {max_iter})"
            else:  # julia
                c = complex(float(julia_real), float(julia_imag))
                iterations = FractalCalculator.compute_julia(
                    width, height, c, max_iter, x_min, x_max, y_min, y_max
                )
                title = f"Julia set (c={c}, Rozlišení: {width}x{height}, Max. iterací: {max_iter})"

            # normalizace iterací pro barevné škály
            norm_iterations = np.zeros_like(iterations, dtype=float)
            mask = iterations < max_iter
            if np.any(mask):
                norm_iterations[mask] = np.log(iterations[mask] + 1) / np.log(max_iter)

            fig = go.Figure(data=go.Heatmap(
                z=norm_iterations,
                x=np.linspace(x_min, x_max, width),
                y=np.linspace(y_min, y_max, height),
                colorscale=colorscale,
                showscale=False,
                hoverinfo='none'
            ))

            fig.update_layout(
                title=title,
                xaxis=dict(
                    title='Re(z)',
                    constrain='domain',
                    scaleanchor='y',
                    scaleratio=1
                ),
                yaxis=dict(
                    title='Im(z)',
                    constrain='domain'
                ),
                margin=dict(l=10, r=10, t=50, b=10),
                uirevision=fractal_type  # Zachová stav přiblížení při změně parametrů
            )

            end_time = time.time()
            computation_time = end_time - start_time

            view_state[fractal_type] = {'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max}

            return fig, f"Vypočteno za {computation_time:.2f} sekund"
