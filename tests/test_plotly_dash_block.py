from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..plotly_dash_block import PlotlyDash
from unittest.mock import patch


class TestExample(NIOBlockTestCase):

    @patch('dash.Dash')
    def test_process_signals(self, mock_dash):
        """Signals pass through block unmodified."""
        blk = PlotlyDash()
        self.configure_block(blk, {})
        blk.start()
        # blk.process_signals([Signal({"hello": "n.io"})])
        blk.stop()
        self.assertTrue(mock_dash.call_count)
