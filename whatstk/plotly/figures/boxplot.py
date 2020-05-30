"""Boxplot figures."""


import plotly.graph_objs as go
import plotly.express as px


def fig_boxplot_msglen(df, title="", xlabel=None):
    """Visualize boxplot.

    Args:
        df (pandas.DataFrame): Chat data.
        title (str, optional): Title for plot. Defaults to "".
        xlabel (str, optional): x-axis label title. Defaults to None.

    Returns:
        dict: Figure.

    Example:

        ```python
        >>> from whatstk.plotly import plot
        >>> from whatstk import df_from_txt
        >>> from whatstk.plot import build_figure_boxplot_msglen
        >>> filename = 'path/to/samplechat.txt'
        >>> df = df_from_txt(filename)
        >>> fig = build_figure_boxplot_msglen(df, 'Message length')
        >>> plot(fig)
        ```

    """
    # Get message lengths
    df['message_length'] = df['message'].apply(lambda x: len(x))
    # Sort users by median
    user_stats = df.groupby('username')\
        .aggregate({'message_length': 'median'})['message_length'].sort_values(ascending=False)

    # Create a list of traces
    data = []

    for username in user_stats.index:
        x = df[df['username'] == username]['message_length']
        trace = go.Box(
            y=x.values,
            showlegend=True,
            name=username,
            boxpoints='outliers'
        )
        data.append(trace)

    layout = dict(
        title=title,
        xaxis=dict(title=xlabel),
        colorway=px.colors.cyclical.mygbm
    )

    return dict(data=data, layout=layout)
