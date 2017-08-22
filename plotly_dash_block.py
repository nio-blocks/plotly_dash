import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
from time import sleep
from flask import request
from dash.dependencies import Output, Event

from nio.block.base import Block
from nio.properties import VersionProperty, FloatProperty, Property, \
    StringProperty, IntProperty, PropertyHolder, ListProperty
from nio.util.threading.spawn import spawn


class Series(PropertyHolder):
    y_axis = Property(
        title='Dependent Variable', default='{{ $y_data }}', allow_none=False)
    name = StringProperty(
        title='Series Name', default='default name', allow_none=False)

class PlotlyDash(Block):

    version = VersionProperty('0.1.0')
    graph_series = ListProperty(Series, title='Data Series', default=[])
    x_axis = Property(
        title='Independent Variable',
        default='{{ datetime.datetime.utcnow() }}',
        allow_none=False
    )
    title = StringProperty(
        title='Title', default='Plotly Title', allow_none=False)
    num_data_points = IntProperty(
        title='How many points to display', default=20, allow_none=True)
    port = IntProperty(title='Port', default=8050)

    def __init__(self):
        self._main_thread = None
        self.app = dash.Dash()
        # self.app.config.supress_callback_exceptions=True
        self.data_dict = {}
        self.data = []
        super().__init__()

    def start(self):
        self._main_thread = spawn(self._server)
        self.logger.debug('server started on localhost:{}'.format(self.port()))

        self.data_dict = {
            s.name(): {'x': [], 'y': [], 'name': s.name()}
            for s in self.graph_series()
        }
        self.data = self.data_dict_to_data_list(self.data_dict)
        figure = {'data': self.data, 'layout': {'title': self.title()}}
        app_layout = [
            dcc.Graph(id=self.title(), figure=figure),
            dcc.Interval(id='interval-component', interval=1 * 1000)
        ]

        self.app.layout = html.Div(app_layout)

        @self.app.callback(Output(self.title(), 'figure'),
                           events=[Event('interval-component', 'interval')])
        def update_graph_live():
            return {'data': self.data, 'layout': {'title': self.title()}}

        @self.app.server.route('/shutdown', methods=['GET'])
        def shutdown():
            shutdown_server()
            return 'OK'

        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                self.logger.warning('Not running with the Werkzeug Server')
            func()
        sleep(0.25)
        super().start()


    def stop(self):
        # http://flask.pocoo.org/snippets/67/
        try:
            r = requests.get('http://localhost:{}/shutdown'.format(
                self.port()))
            self.logger.debug('shutting down server ...')
        except:
            self.logger.warning('shutdown_server callback failed')
        try:
            self._main_thread.join()
            self.logger.debug('_main_thread joined')
        except:
            self.logger.warning('_main_thread exited before join() call')
        if self._main_thread.is_alive():
            self.logger.warning('_main_thread did not exit')
        super().stop()

    def process_signals(self, signals):
        # process_signals just needs to update self.data list
        # append new signal data to the proper dict key
        for signal in signals:
            for series in self.graph_series():
                if not isinstance(self.x_axis(signal), list):
                    if len(self.data_dict[series.name()]['y']) \
                            < self.num_data_points():
                        self.data_dict[series.name()]['x'].append(
                            self.x_axis(signal))
                        self.data_dict[series.name()]['y'].append(
                            series.y_axis(signal))
                    else:
                        self.data_dict[series.name()]['x'].append(
                            self.x_axis(signal))
                        self.data_dict[series.name()]['y'].append(
                            series.y_axis(signal))
                        self.data_dict[series.name()]['x'] = \
                            self.data_dict[series.name()]['x'][1:]
                        self.data_dict[series.name()]['y'] = \
                            self.data_dict[series.name()]['y'][1:]
                else:
                    self.data_dict[series.name()]['x'] = self.x_axis(signal)
                    self.data_dict[series.name()]['y'] = series.y_axis(signal)

        self.data = self.data_dict_to_data_list(self.data_dict)

    @staticmethod
    def data_dict_to_data_list(dict):
        return [v for d,v in dict.items()]

    def _server(self):
        self.app.layout = html.Div()
        # if debug isn't passed the server breaks silently
        self.app.run_server(debug=False, port=self.port(), host='0.0.0.0')
