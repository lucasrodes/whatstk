"""Plot tools using plotly.

Import :func:`plot <whatstk.graph.plot>` to plot figures.

..  code-block:: python

    >>> from whatstk.graph import plot

"""

try:
    from plotly.offline import plot
    import plotly.io as pio

    from whatstk.graph.base import FigureBuilder
except ImportError as e:  # pragma: no cover
    msg = (  # pragma: no cover
        "whatstk plotting requirements are not installed.\n\n"
        "Please pip install as follows:\n\n"
        '  python -m pip install "whatstk[viz]" --upgrade'
    )  # pragma: no cover
    raise ImportError(msg) from e  # pragma: no cover


pio.templates.default = "plotly_white"


__all__ = ["plot", "FigureBuilder"]
