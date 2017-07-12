from nio.block.base import Block
from nio.properties import VersionProperty
import dash
import dash_core_components as dcc
# import dash_html_components as html


class PlotlyDash(Block):

    version = VersionProperty('0.1.0')

    def __init__(self):
        self.app = None
        super().__init__()

    def setUp(self):
        self.app = dash.Dash()
        super().setUp()

    def process_signals(self, signals):
        for signal in signals:
            pass
        self.notify_signals(signals)
