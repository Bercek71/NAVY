import dash
import numpy as np
from dash import html, dcc, Output, Input
from plotly import express as px

from ForestFire import ForestFire


class ForestFireApp:
    def __init__(self):
        self.app = dash.Dash(__name__, update_title=None)
        self.server = self.app.server
        self.simulation = ForestFire()
        self._setup_layout()
        self._setup_callbacks()

    def _setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Forest Fire Cellular Automaton", style={"textAlign": "center"}),
            html.Div([
                html.Div([
                    html.Label("Growth Probability (p):"),
                    dcc.Slider(
                        id="p-slider",
                        min=0,
                        max=0.1,
                        step=0.001,
                        value=self.simulation.p,
                        marks={i / 100: f"{i / 100}" for i in range(0, 11, 2)},
                    ),
                    html.Label("Fire Probability (f):"),
                    dcc.Slider(
                        id="f-slider",
                        min=0,
                        max=0.01,
                        step=0.0001,
                        value=self.simulation.f,
                        marks={i / 1000: f"{i / 1000}" for i in range(0, 11, 2)},
                    ),
                    html.Label("Neighborhood:"),
                    dcc.RadioItems(
                        id="neighborhood-radio",
                        options=[
                            {"label": "Von Neumann", "value": False},
                            {"label": "Moore", "value": True},
                        ],
                        value=self.simulation.use_moore,
                        labelStyle={"display": "inline-block", "margin-right": "10px"},
                    ),
                    html.Button("Reset Simulation", id="reset-button", style={"marginTop": "10px"}),
                ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

                html.Div([
                    dcc.Graph(id="forest-fire-graph", style={"height": "80vh"}),
                ], style={"width": "70%", "display": "inline-block"}),
            ]),

            dcc.Interval(
                id="interval-component",
                interval=200,
                n_intervals=0,
            ),
            dcc.Store(id="grid-store", data=self.simulation.grid.tolist()),
        ])

    def _setup_callbacks(self):
        @self.app.callback(
            Output("grid-store", "data"),
            [Input("reset-button", "n_clicks"),
             Input("p-slider", "value"),
             Input("f-slider", "value"),
             Input("neighborhood-radio", "value")],
            prevent_initial_call=True,
        )
        def reset_simulation(n_clicks, p, f, use_moore):
            if n_clicks:
                return self.simulation.reset(p, f, use_moore).tolist()
            return dash.no_update

        @self.app.callback(
            [Output("grid-store", "data", allow_duplicate=True),
             Output("forest-fire-graph", "figure")],
            [Input("interval-component", "n_intervals")],
            [dash.dependencies.State("grid-store", "data"),
             dash.dependencies.State("p-slider", "value"),
             dash.dependencies.State("f-slider", "value"),
             dash.dependencies.State("neighborhood-radio", "value")],
            prevent_initial_call=True,
        )
        def update_simulation(n_intervals, stored_grid, p, f, use_moore):
            self.simulation.grid = np.array(stored_grid)
            self.simulation.p = p
            self.simulation.f = f
            self.simulation.use_moore = use_moore

            new_grid = self.simulation.update()

            fig = px.imshow(
                new_grid,
                color_continuous_scale=self.simulation.color_scale,
                zmin=0,
                zmax=3,
            )

            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                coloraxis_showscale=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )

            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            return new_grid.tolist(), fig

    def run(self, debug=True):
        self.app.run(debug=debug)
