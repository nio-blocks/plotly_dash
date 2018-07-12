PlotlyDash
==========
Create webserver and plot data series using Plot.ly-Dash on a locally hosted webpage.

Plot multiple lines on the same graph, and take advantage of all of Plot.ly's built in browser interactivity.

*Known bug*: Race condition exists during service start.  It's possible that graph is not full built by the time a signal is received, in which case the signal will not be plotted.  Make sure the block has fully started before calling process_signals.

Properties
----------
- **graph_series**: Lines to plot on the graph. Supply a dependent (Y-axis) variable and name per line.
- **num_data_points**: How many previous data points will be displayed on the graph.
- **port**: Port on which to run the local webserver.
- **title**: The graph's title.
- **update_interval**: How often to update the graph.
- **x_axis**: The independent (X-axis) variable.

Inputs
------
- **default**: Any list of signals containing data to be plotted.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
None

