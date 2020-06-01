"""Plot utils."""


from whatstk.graph.figures.scatter import fig_scatter_time
import warnings


def vis(user_data, title):
    """See method `vis_scatter_time`.

    Args:
        user_data (pandas.DataFrame): Input data.
        title (str): Title of figure.

    Returns:
        dict: Figure.

    """
    warnings.warn("Will be deprecated in 0.4.0. Use whatstk.graph.FigureBuilder instead.", FutureWarning)
    return fig_scatter_time(user_data=user_data, title=title)
