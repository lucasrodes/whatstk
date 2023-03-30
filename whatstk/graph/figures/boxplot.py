"""Boxplot figures."""

from typing import Dict, Optional

import plotly.graph_objs as go
import pandas as pd

from whatstk.utils.utils import COLNAMES_DF


def fig_boxplot_msglen(
    df: pd.DataFrame, username_to_color: Dict[str, str] = None, title: str = "", xlabel: Optional[str] = None
) -> go.Figure:
    """Visualize boxplot.

    Args:
        df (pandas.DataFrame): Chat data.
        username_to_color (dict, optional). Dictionary mapping username to color. Defaults to None.
        title (str, optional): Title for plot. Defaults to "".
        xlabel (str, optional): x-axis label title. Defaults to None.

    Returns:
        plotly.graph_objs.Figure

    """
    df = df.copy()
    # Get message lengths
    df[COLNAMES_DF.MESSAGE_LENGTH] = df[COLNAMES_DF.MESSAGE].apply(lambda x: len(x))
    # Sort users by median
    user_stats = (
        df.groupby(COLNAMES_DF.USERNAME)
        .aggregate({COLNAMES_DF.MESSAGE_LENGTH: "median"})[COLNAMES_DF.MESSAGE_LENGTH]
        .sort_values(ascending=False)
    )

    # Create a list of traces
    data = []

    for username in user_stats.index:
        x = df[df[COLNAMES_DF.USERNAME] == username][COLNAMES_DF.MESSAGE_LENGTH]
        trace = go.Box(
            y=x.values,
            showlegend=True,
            name=username,
            boxpoints="outliers",
            marker_color=username_to_color[username] if username_to_color else None,
        )
        data.append(trace)

    layout = dict(title=title, xaxis=dict(title=xlabel))

    fig = go.Figure(data=data, layout=layout)

    return fig
