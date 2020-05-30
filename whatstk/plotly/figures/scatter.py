"""Scatter plot figures."""


import plotly.graph_objs as go


def fig_scatter_time(user_data, username_to_color=None, title="", xlabel=None):
    """Obtain Figure to plot using plotly.

    `user_data` must be a pandas.DataFrame with timestamps as index and a column for each user.

    Note: Does not work with output of `get_interventions_count` if date_mode='hourweekday'.

    Args:
        user_data (pandas.DataFrame): Input data. Shape nrows x ncols, where nrows = number of timestaps and
                                      ncols = number of users.
        username_to_color (dictm optional). Dictionary mapping username to color. Defaults to None.
        title (str, optional): Title of figure. Defaults to "".
        xlabel (str, optional): x-axis label title. Defaults to None.

    Returns:
        dict: Figure.

    Example:

        ```python
        >>> from plotly.offline import plot
        >>> from whatstk import df_from_txt
        >>> from whatstk.analysis import interventions
        >>> from whatstk.plot import build_figure_scatter_time
        >>> filename = 'path/to/samplechat.txt'
        >>> df = df_from_txt(filename)
        >>> counts = interventions(df=df, date_mode='date', msg_length=False, cummulative=True)
        >>> fig = build_figure_scatter_time(counts, 'cumulative number of messages sent per day')
        >>> plot(fig)
        ```

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
            line=dict(color=username_to_color[username])
        )
        data.append(trace)

    layout = dict(
        title=title,
        xaxis=dict(title=xlabel)
    )

    return dict(data=data, layout=layout)
