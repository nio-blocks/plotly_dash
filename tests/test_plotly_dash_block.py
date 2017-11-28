from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..plotly_dash_block import PlotlyDash


class TestExample(NIOBlockTestCase):

    @patch('dash_html_components.Div')
    @patch('dash_core_components.Graph')
    @patch('dash.Dash')
    def test_process_signals(self, mock_dash, mock_graph, mock_div):
        input_signal1 = [Signal({'y_data': 1, 'x_data': 8})]
        input_signal2 = [Signal({'y_data': 2, 'x_data': 9})]
        graph_instances = [MagicMock(), MagicMock()]
        mock_graph.side_effect = graph_instances
        blk = PlotlyDash()
        self.configure_block(blk, {
            'graphs': [{
                'graph_series': [{
                    'y_axis': '{{ $y_data }}',
                    'name': 'series name'
                }],
                'x_axis': '{{ $x_data }}'
            }]
        })
        blk.start()
        blk.process_signals(input_signal1)
        blk.process_signals(input_signal2)
        blk.stop()

        # Dash() is instantiated
        self.assertEqual(mock_dash.call_count, 1)
        # server is started
        self.assertEqual(mock_dash.return_value.run_server.call_count, 1)
        # Graph() is instantiated
        self.assertEqual(mock_graph.call_count, 1)

        # Div() is instantiated twice, in _server() and start()
        self.assertEqual(mock_div.call_count, 2)

        # self.data is updated to contain correct data from signal
        self.assertEqual(blk.data[0]['x'], [8, 9])
        self.assertEqual(blk.data[0]['y'], [1, 2])


    @patch('dash_html_components.Div')
    @patch('dash_core_components.Graph')
    @patch('dash.Dash')
    def test_process_signals_list(self, mock_dash, mock_graph, mock_div):
        input_signal3 = [Signal({'y_data': [1, 2, 3], 'x_data': [1, 2, 3]})]
        input_signal4 = [Signal({'y_data': [4, 5, 6], 'x_data': [4, 5, 6]})]
        graph_instances = [MagicMock(), MagicMock()]
        mock_graph.side_effect = graph_instances
        blk = PlotlyDash()
        self.configure_block(blk, {
            'graph_series': [{
                'y_axis': '{{ $y_data }}',
                'name': 'series name'
            }],
            'x_axis': '{{ $x_data }}'
        })
        blk.start()
        blk.process_signals(input_signal3)
        blk.process_signals(input_signal4)
        blk.stop()

        # Dash() is instantiated
        self.assertEqual(mock_dash.call_count, 1)
        # server is started
        self.assertEqual(mock_dash.return_value.run_server.call_count, 1)
        # Graph() is instantiated
        self.assertEqual(mock_graph.call_count, 1)

        # Div() is instantiated twice, in _server() and start()
        self.assertEqual(mock_div.call_count, 2)

        # self.data is updated to contain correct data from most recent
        # signal only
        self.assertEqual(blk.data[0]['x'], [4, 5, 6])
        self.assertEqual(blk.data[0]['y'], [4, 5, 6])
