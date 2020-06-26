"""Plot tools using plotly.

Import :func:`plot <whatstk.graph.plot>` to plot figures.

..  code-block:: python
        >>> from whatstk.graph import plot

"""


from plotly.offline import plot
import plotly.io as pio
from whatstk.graph.base import FigureBuilder


pio.templates.default = "plotly_white"


__all__ = [
    'plot',
    'FigureBuilder'
]
