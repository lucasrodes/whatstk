"""Plot utils."""


import plotly.graph_objs as go


def vis(user_data, title):
    """Obtain Figure to plot using plotly.

    Does not work if you use date_mode='hourweekday'.

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
        >>> from whatstk.plot import vis
        >>> plot(vis(counts_cumsum, 'cumulative number of messages sent per day'))
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

    layout = dict(title=title, xaxis=dict(title='Date'))

    return dict(data=data, layout=layout)
