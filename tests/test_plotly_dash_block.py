from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..plotly_dash_block import PlotlyDash
from unittest.mock import patch, MagicMock, ANY


class TestExample(NIOBlockTestCase):

    @patch('dash_html_components.Div')
    @patch('dash_core_components.Graph')
    @patch('dash.Dash')
    def test_process_signals(self, mock_dash, mock_graph, mock_div):
        input_signals = [
            Signal({'title': '1', 'data': {'foo1': 'bar1'}}),
            Signal({'title': '2', 'data': {'foo2': 'bar2'}})]
        graph_instances = [MagicMock(), MagicMock()]
        mock_graph.side_effect = graph_instances
        blk = PlotlyDash()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(input_signals)
        blk.stop()

        # Dash() is instantiated
        self.assertTrue(mock_dash.call_count)
        # server is started
        self.assertTrue(mock_dash.return_value.run_server.call_count)
        # Graph() is instantiated for each signal
        self.assertEqual(mock_graph.call_count, len(input_signals))
        graph_args = [args[1] for args in mock_graph.call_args_list]
        for arg in graph_args:
            # todo: assert actual values instead of ANY
            self.assertDictEqual({'id': ANY, 'figure': {'data': ANY, 'layout': {'title': ANY}}}, arg)
        # Div() is instantiated with instanvces of Graph()
        self.assertTrue(mock_div.call_count)
        self.assertEqual(mock_div.call_args[1]['children'], graph_instances)
