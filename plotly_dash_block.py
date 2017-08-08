import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event

from nio.block.base import Block
from nio.properties import VersionProperty, FloatProperty, Property, \
    StringProperty, IntProperty
from nio.util.threading.spawn import spawn


class PlotlyDash(Block):


    version = VersionProperty('0.1.0')
    title = StringProperty(
        title="Title", default="Plotly Title", allow_none=False)
    x_axis = Property(
        title="X axis value",
        default="{{ datetime.datetime.utcnow() }}",
        allow_none=False
    )
    y_axis = FloatProperty(
        title="Y axis value", default="{{ $y_data }}", allow_none=False)
    num_data_points = IntProperty(
        title="How many points to display", default=20, allow_none=True)

    def __init__(self):
        self._main_thread = None
        self.app = dash.Dash()
        self.app.config.supress_callback_exceptions=True
        self.data = {
            "x": [],
            "y": []
        }
        super().__init__()

    def start(self):
        self._main_thread = spawn(self._server)
        self.logger.debug('server started on localhost:8050')
        super().start()

        figure = {'data': [self.data], 'layout': {'title': self.title()}}
        self.app.layout = html.Div(
            [dcc.Graph(id=self.title(), figure=figure),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000  # in milliseconds
            )]
        )
        @self.app.callback(Output(self.title(), 'figure'),
                           events=[Event('interval-component', 'interval')])
        def update_graph_live():
            return {'data': [self.data], 'layout': {'title': self.title()}}


    def stop(self):
        try:
            self._main_thread.join(1)
            self.logger.debug('server stopped')
        except:
            self.logger.warning('main thread exited before join()')
        super().stop()

    def process_signals(self, signals):
        graphs = []
        for signal in signals:
            if len(self.data["x"]) < self.num_data_points():
                self.data["x"].append(self.x_axis(signal))
                self.data["y"].append(self.y_axis(signal))
            else:
                self.data["x"].append(self.x_axis(signal))
                self.data["y"].append(self.y_axis(signal))
                self.data["x"] = self.data["x"][1:]
                self.data["y"] = self.data["y"][1:]
        self.logger.debug('displaying {} graphs '.format(len(graphs)))

    def _server(self):
        self.app.layout = html.Div()
        self.app.run_server(debug=False)
