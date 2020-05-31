"""Sankey plot figures."""


import plotly.graph_objs as go


def fig_sankey(label, color, source, target, value, title=""):
    """Generate sankey image.

    Args:
        label (list): List with node labels.
        color (list): List with node colors.
        source (list): List with link source id.
        target (list): List with linke target id.
        value (list): List with link value.
        title (str, optional): Title. Defaults to "".

    Returns:
        dict: Figure as dictionary.

    """
    trace = go.Sankey(
        arrangement='fixed',
        orientation='v',
        valueformat=".0f",
        node=dict(
            pad=20,
            thickness=40,
            line=dict(
                color="black",
                width=0
            ),
            label=label,
            color=color,
            hovertemplate="%{label}<br>Number of messages: %{value}<extra></extra>",
            # x=x,
            # y=y
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            hovertemplate="%{source.label} ---> %{target.label}<extra>%{value}</extra>"
        )
    )
    data = [trace]

    layout = {
        'title': dict(text=title),
        'annotations': [
            {
                'text': "Senders",
                'font': {
                    'size': 13,
                    'color': 'rgb(116, 101, 130)',
                },
                'showarrow': False,
                'align': 'center',
                'x': 0.5,
                'y': 1.1,
                'xref': 'paper',
                'yref': 'paper',
            },
            {
                'text': "Receivers",
                'font': {
                    'size': 13,
                    'color': 'rgb(116, 101, 130)',
                },
                'showarrow': False,
                'align': 'center',
                'x': 0.5,
                'y': -.1,
                'xref': 'paper',
                'yref': 'paper',
            }
        ]
    }

    fig = dict(data=data, layout=layout)

    return fig
