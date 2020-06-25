"""Scatter plot figures."""


import plotly.graph_objs as go


def fig_scatter_time(user_data, username_to_color=None, title="", xlabel=None):
    """Obtain Figure to plot using plotly.

    ``user_data`` must be a pandas.DataFrame with timestamps as index and a column for each user. You can easily
    generate suitable ``user_data`` using the function
    :func:`get_interventions_count <whatstk.analysis.get_interventions_count>` (disclaimer: not compatible with
    ``date_mode='hourweekday'``).

    Args:
        user_data (pandas.DataFrame): Input data. Shape nrows x ncols, where nrows = number of timestaps and
                                      ncols = number of users.
        username_to_color (dict, optional). Dictionary mapping username to color. Defaults to None.
        title (str, optional): Title of figure. Defaults to "".
        xlabel (str, optional): x-axis label title. Defaults to None.

    Returns:
        plotly.graph_objs.Figure

    ..  seealso::

            * :func:`get_interventions_count <whatstk.analysis.get_interventions_count>`

    """
    # Create a trace
    data = []

    for username in user_data:
        trace = go.Scatter(
            x=user_data.index,
            y=user_data[username],
            showlegend=True,
            name=username,
            text=user_data.index,
            line=dict(color=username_to_color[username]) if username_to_color is not None else None
        )
        data.append(trace)

    layout = dict(
        title=title,
        xaxis=dict(title=xlabel)
    )

    fig = go.Figure(data=data, layout=layout)

    return fig
