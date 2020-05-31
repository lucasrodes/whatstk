"""Heatmap plot figures."""


import plotly.graph_objs as go


def fig_heatmap(df_matrix, title=""):
    """Generate heatmap figure from NxN matrix.

    Args:
        df_matrix (pandas.DataFrame): Matrix as DataFrame. Index values and column values must be equal.
        title (str): Title of plot. Defaults to "".

    Returns:
        [type]: [description]
    """
    trace = go.Heatmap(
        z=df_matrix,
        x=df_matrix.columns,
        y=df_matrix.index,
        hovertemplate='%{y} ---> %{x}<extra>%{z}</extra>',
        colorscale='Greens'
    )
    data = [trace]
    layout = {
        'title': {'text': title},
        'xaxis': {'title': "Receiver"},
        'yaxis': {'title': "Sender"}
    }
    fig = dict(data=data, layout=layout)
    return fig
