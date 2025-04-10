import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

class FractalVisualizer:

    def __init__(self, model = None):

        self.model = model

    def set_model(self, model):

        self.model = model

    def create_static_plot(self, num_points = 50000,
                           marker_size = 2.0,
                           opacity = 0.7,
                           reset_history = True):

        if self.model is None:
            raise ValueError("No fractal model set for visualization")

        if reset_history:
            self.model.generate_points(num_points)

        x, y, z = self.model.get_history_arrays()

        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=marker_size,
                color=z,
                colorscale='Viridis',
                opacity=opacity
            )
        )])

        fig.update_layout(
            title=f"{self.model.name} - {len(x)} Points",
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        return fig

    def save_plot(self, filename, fig = None,
                  num_points = 50000, width = 800, height = 800):

        if fig is None:
            fig = self.create_static_plot(num_points)

        fig.write_html(f"{filename}.html", auto_open=False)
        fig.write_image(f"{filename}.png", width=width, height=height)


def create_dash_app(model1, model2, points_per_step=100, max_points=20000):

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("3D Fractal Explorer"),

        html.Div([
            html.Div([
                html.H3("Controls"),
                html.Button('Start Animation', id='animate-button', n_clicks=0),
                html.Button('Reset', id='reset-button', n_clicks=0),
                html.Div([
                    html.Label("Points per step:"),
                    dcc.Slider(
                        id='points-slider',
                        min=10,
                        max=500,
                        step=10,
                        value=points_per_step,
                        marks={i: str(i) for i in range(0, 501, 100)}
                    )
                ], style={'margin-top': '20px', 'margin-bottom': '20px'}),
                html.Div([
                    html.Label("Animation speed (ms):"),
                    dcc.Slider(
                        id='speed-slider',
                        min=100,
                        max=2000,
                        step=100,
                        value=500,
                        marks={i: str(i) for i in range(0, 2001, 500)}
                    )
                ], style={'margin-bottom': '20px'}),
                html.Div([
                    html.Label("Select Model:"),
                    dcc.RadioItems(
                        id='model-selector',
                        options=[
                            {'label': model1.name, 'value': 'model1'},
                            {'label': model2.name, 'value': 'model2'}
                        ],
                        value='model1'
                    )
                ], style={'margin-bottom': '20px'}),
                html.Div(id='stats-display', style={'margin-top': '20px'})
            ], style={'width': '25%', 'float': 'left', 'padding': '20px'}),

            html.Div([
                dcc.Graph(id='fractal-plot', style={'height': '80vh'}),
                dcc.Interval(
                    id='interval-component',
                    interval=500,
                    n_intervals=0,
                    disabled=True
                ),
                html.Div(id='points-count', style={'margin-top': '10px'})
            ], style={'width': '75%', 'float': 'right'})
        ], style={'display': 'flex', 'flex-direction': 'row'})
    ])

    model1.reset_history()
    model2.reset_history()

    @app.callback(
        Output('interval-component', 'disabled'),
        Input('animate-button', 'n_clicks'),
        Input('reset-button', 'n_clicks'),
        State('interval-component', 'disabled')
    )
    def toggle_animation(animate_clicks, reset_clicks, currently_disabled):
        ctx = dash.callback_context
        if not ctx.triggered:
            return currently_disabled

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'animate-button':
            return not currently_disabled
        elif button_id == 'reset-button':
            return True

        return currently_disabled

    @app.callback(
        Output('interval-component', 'interval'),
        Input('speed-slider', 'value')
    )
    def update_interval(value):
        return value

    @app.callback(
        Output('fractal-plot', 'figure'),
        Output('points-count', 'children'),
        Output('stats-display', 'children'),
        Input('interval-component', 'n_intervals'),
        Input('reset-button', 'n_clicks'),
        Input('model-selector', 'value'),
        State('points-slider', 'value')
    )
    def update_plot(n_intervals, reset_clicks, model_selection, points_per_step):
        ctx = dash.callback_context
        if not ctx.triggered:
            model = model1 if model_selection == 'model1' else model2
            model.reset_history()
            model.generate_points(100, skip_initial=20)
        else:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            model = model1 if model_selection == 'model1' else model2

            if trigger_id == 'reset-button':
                model.reset_history()
                model.generate_points(100, skip_initial=20)
            elif trigger_id == 'model-selector':
                if len(model.point_history) == 0:
                    model.generate_points(100, skip_initial=20)
            elif trigger_id == 'interval-component':
                for _ in range(points_per_step):
                    model.generate_next_point()

                if len(model.point_history) > max_points:
                    model.point_history = model.point_history[-max_points:]
                    model.transformation_history = model.transformation_history[-max_points:]

        model = model1 if model_selection == 'model1' else model2
        x, y, z = model.get_history_arrays()

        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=2,
                color=z,
                colorscale='Viridis',
                opacity=0.7
            )
        )])

        fig.update_layout(
            title=f"{model.name} - Interactive Explorer",
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=40),
           # uirevision='constant'
        )

        stats = model.get_stats()
        stats_display = html.Div([
            html.H4("Statistics"),
            html.P(f"Total Points: {stats['points']}"),
            html.H5("Transformation Usage:"),
            html.Ul([
                html.Li(f"{name}: {data['count']} ({data['percentage']:.1f}%)")
                for name, data in stats['transformations'].items()
            ])
        ])

        return fig, f"Displaying {len(x)} points", stats_display

    return app

