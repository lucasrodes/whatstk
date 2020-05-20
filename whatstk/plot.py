"""Plot utils."""


import plotly.graph_objs as go
import warnings


def vis_boxplot(user_data, title, ignore_zero=True):

    # Create a trace
    data = []

    for username in user_data:
        trace = go.Box(
            x=user_data.index,
            y=user_data[username],
            showlegend=True,
            name=username,
            text=user_data.index
        )
        data.append(trace)

    layout = dict(title=title, xaxis=dict(title='Date'))

    return dict(data=data, layout=layout)


def vis_scatter_time(user_data, title, xlabel=None):
    """Obtain Figure to plot using plotly.

    `user_data` must be a pandas.DataFrame with timestamps as index and a column for each user.

    Note: Does not work with output of `interventions` if date_mode='hourweekday'.

    Args:
        user_data (pandas.DataFrame): Input data.
        title (str): Title of figure.

    Returns:
        dict: Figure.

    Example:

        ```python
        >>> from whatstk import df_from_txt
        >>> from whatstk.analysis import interventions
        >>> filename = 'path/to/samplechat.txt'
        >>> df = df_from_txt(filename)
        >>> counts = interventions(df=df, date_mode='date', msg_length=False)
        >>> counts_cumsum = counts.cumsum()
        >>> from plotly.offline import plot
        >>> from whatstk.plot import vis_scatter_time
        >>> plot(vis_scatter_time(counts_cumsum, 'cumulative number of messages sent per day'))
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
            text=user_data.index
        )
        data.append(trace)

    layout = dict(title=title, xaxis=dict(title=xlabel))

    return dict(data=data, layout=layout)


def vis(user_data, title):
    """See method `vis_scatter_time`.

    Args:
        user_data (pandas.DataFrame): Input data.
        title (str): Title of figure.

    Returns:
        dict: Figure.

    """
    warnings.warn("Will be deprecated in 0.4.0. Use scatter_vis instead.", FutureWarning)
    return vis_scatter_time(user_data, title)

