from nio.block.base import Block
from nio.properties import VersionProperty
import dash
import dash_core_components as dcc
import dash_html_components as html


class PlotlyDash(Block):

    version = VersionProperty('0.1.0')

    def __init__(self):
        self.app = dash.Dash()
        super().__init__()

    def start(self):
        self.app.layout = html.Div()
        self.app.run_server(debug=False)
        super().start()

    def process_signals(self, signals):
        graphs = []
        for signal in signals:
            graphs.append(dcc.Graph(id=signal.title, figure={'data': [signal.data], 'layout': {'title': signal.title}}))
        self.app.layout = html.Div(children=graphs)
