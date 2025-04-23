import dash_bootstrap_components as dbc
from dash import html, dcc

from FractalAppConfig import FractalAppConfig


class FractalView:

    @staticmethod
    def create_layout():
        return dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Fractal explorer", className="text-center my-4"), width=12)
            ]),

            dbc.Row([
                dbc.Col([
                    # typ fraktálu
                    html.Label("Fraktál:"),
                    dcc.RadioItems(
                        id='fractal-type',
                        options=[
                            {'label': 'Mandelbrot set', 'value': 'mandelbrot'},
                            {'label': 'Julia set', 'value': 'julia'}
                        ],
                        value='mandelbrot',
                        inline=True,
                        className="mb-3"
                    ),

                    # julia parametry
                    html.Div([
                        html.Label("Parametry julia set:"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Reálná část:"),
                                dcc.Input(
                                    id='julia-real',
                                    type='number',
                                    value=-0.7,
                                    step=0.01,
                                    className="form-control"
                                )
                            ], width=6),
                            dbc.Col([
                                html.Label("Imaginární část:"),
                                dcc.Input(
                                    id='julia-imag',
                                    type='number',
                                    value=0.27,
                                    step=0.01,
                                    className="form-control"
                                )
                            ], width=6)
                        ]),
                        html.Button('Randomize parameters', id='random-julia', className="btn btn-primary my-2")
                    ], id='julia-params', style={'display': 'none'}),

                    html.Label("Maximální počet iterací:"),
                    dcc.Slider(
                        id='max-iter-slider',
                        min=50,
                        max=500,
                        step=50,
                        value=FractalAppConfig.DEFAULT_MAX_ITER,
                        marks={50: '50', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500'},
                        className="mb-3"
                    ),

                    html.Label("Rozlišení:"),
                    dcc.Slider(
                        id='resolution-slider',
                        min=100,
                        max=1000,
                        step=100,
                        value=FractalAppConfig.DEFAULT_WIDTH,
                        marks={100: 'Nízké', 500: 'Střední', 1000: 'Vysoké'},
                        className="mb-3"
                    ),

                    html.Label("Barvy:"),
                    dcc.Dropdown(
                        id='colorscale',
                        options=[{'label': cs, 'value': cs} for cs in FractalAppConfig.COLORSCALES],
                        value=FractalAppConfig.DEFAULT_COLORSCALE,
                        clearable=False,
                        className="mb-3"
                    ),

                    html.Button('Resetovat pohled', id='reset-view', className="btn btn-danger my-2 w-100"),

                    html.Div(id='performance-info', className="mt-3 text-muted"),

                ], width=3),

                dbc.Col([
                    # graf fraktálu
                    dcc.Graph(
                        id='fractal-graph',
                        style={'height': '80vh'},
                        config={
                            'scrollZoom': True,
                            'displayModeBar': True,
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                        }
                    ),

                    # ukládání stavu pohledu
                    dcc.Store(id='view-state', data={
                        'mandelbrot': FractalAppConfig.DEFAULT_MANDELBROT_VIEW.copy(),
                        'julia': FractalAppConfig.DEFAULT_JULIA_VIEW.copy()
                    })
                ], width=9)
            ])
        ], fluid=True)
