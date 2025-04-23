import dash_bootstrap_components as dbc
from dash import Dash

from FractalView import FractalView
from FractalCallbacks import FractalCallbacks


class FractalApp:

    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.layout = FractalView.create_layout()
        FractalCallbacks.register_callbacks(self.app)

    def run(self, debug=True):
        self.app.run(debug=debug)
