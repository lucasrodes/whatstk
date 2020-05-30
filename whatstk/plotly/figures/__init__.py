"""Build Plotly compatible Figures."""


from whatstk.plotly.figures.base import FigureBuilder
import plotly.io as pio


pio.templates.default = "plotly_white"


__all__ = [
    'FigureBuilder'
]
