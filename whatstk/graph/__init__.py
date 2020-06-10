"""Plot tools using plotly."""


from plotly.offline import plot
import plotly.io as pio
from whatstk.graph.base import FigureBuilder


pio.templates.default = "plotly_white"


__all__ = [
    'plot',
    'FigureBuilder'
]
