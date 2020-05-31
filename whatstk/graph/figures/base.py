"""Build plotly-compatible figures."""


import numpy as np
from whatstk.objects import WhatsAppChat
from whatstk.analysis import get_interventions_count, response_matrix
from whatstk.graph.figures.scatter import fig_scatter_time
from whatstk.graph.figures.boxplot import fig_boxplot_msglen
from whatstk.graph.figures.sankey import fig_sankey
from whatstk.graph.figures.heatmap import fig_heatmap
from whatstk.graph.figures.utils import hex_color_palette
from whatstk.utils.utils import _get_df


class FigureBuilder:
    """Generate a variety of figures from your loaded chat."""

    def __init__(self, df=None, chat=None):
        """Constructor.

        Args:
            df (pandas.DataFrame, optional): Chat data. Atribute `df` of a chat loaded using WhatsAppChat. Defaults to
                                             None.
            chat (WhatsAppChat, optional): Chat data. Object obtained when chat loaded using WhatsAppChat. Defaults to
                                           None.
            title (str, optional): Figure title. Defaults to "".
            xlabel (str, optional): x-axis label. Defaults to None.

        """
        self.df = _get_df(df=df, chat=chat)

    @property
    def usernames(self):
        """Get list with users available in given chat.

        Returns:
            list: List with usernames available in chat DataFrame.

        """
        return WhatsAppChat(df=self.df).users

    @property
    def user_color_mapping(self):
        """Build mapping between user and color.

        Returns:
            dict: Mapping username -> color (rgb).

        """
        colors = hex_color_palette(n_colors=len(self.usernames))
        mapping = dict(zip(self.usernames, colors))
        return mapping

    def user_msg_length_boxplot(self, title="User message length", xlabel="User"):
        """Get boxplot of message length of all users.

        Returns:
            dict: Dictionary with data and layout. Plotly compatible
            title (str, optional): Title for plot. Defaults to "User message length".
            xlabel (str, optional): x-axis label title. Defaults to "User".

        Example:

            ```python
            >>> from whatstk import df_from_txt
            >>> from whatstk.graph import plot, FigureBuilder
            >>> filename = 'path/to/samplechat.txt'
            >>> df = df_from_txt(filename)
            >>> fig = FigureBuilder(df).user_msg_length_boxplot()
            >>> plot(fig)
            ```

        """
        fig = fig_boxplot_msglen(
            df=self.df,
            username_to_color=self.user_color_mapping,
            title=title,
            xlabel=xlabel
        )
        return fig

    def user_interventions_count_linechart(self, date_mode='date', msg_length=False, cummulative=False,
                                           title="User interventions count", xlabel="Date/Time"):
        """Plot number of user interventions over time.

        Args:
            date_mode (str, optional): Choose mode to group interventions by. Defaults to 'date'. Available modes are:
                            - 'date': Grouped by particular date (year, month and day).
                            - 'hour': Grouped by hours.
                            - 'month': Grouped by months.
                            - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
                            - 'hourweekday': Grouped by weekday and hour.
            msg_length (bool, optional): Set to True to count the number of characters instead of number of messages
                                         sent.
            cummulative (bool, optional): Set to True to obtain commulative counts.
            title (str, optional): Title for plot. Defaults to "User interventions count".
            xlabel (str, optional): x-axis label title. Defaults to "Date/Time".

        Returns:
            dict: Dictionary with data and layout. Plotly compatible

        Example:

            ```python
            >>> from whatstk import df_from_txt
            >>> from whatstk.graph import plot, FigureBuilder
            >>> filename = 'path/to/samplechat.txt'
            >>> df = df_from_txt(filename)
            >>> fig = FigureBuilder(df).user_interventions_count_linechart(cummulative=True)
            >>> plot(fig)
            ```

        """
        counts = get_interventions_count(
            df=self.df,
            date_mode=date_mode,
            msg_length=msg_length,
            cummulative=cummulative,
        )
        fig = fig_scatter_time(
            user_data=counts,
            username_to_color=self.user_color_mapping,
            title=title,
            xlabel=xlabel
        )
        return fig

    def user_message_responses_flow(self, title="Message flow"):
        """Get the flow of message responses.

        A response is from user X to user Y happens if user X sends a message right after message Y does.

        This method generates a plotly-ready figure (as a dictionary) using Sankey diagram.

        Args:
            title (str, optional): Title for plot. Defaults to "Message flow".

        Returns:
            dict: Dictionary with data and layout. Plotly compatible

        Example:

            ```python
            >>> from whatstk import df_from_txt
            >>> from whatstk.graph import plot, FigureBuilder
            >>> filename = 'path/to/samplechat.txt'
            >>> df = df_from_txt(filename)
            >>> fig = FigureBuilder(df).user_message_responses_flow()
            >>> plot(fig)
            ```

        """
        # Get response matrix
        responses = response_matrix(self.df)

        # Node lists
        label = self.usernames * 2
        color = list(self.user_color_mapping.values())*2
        # Link lists
        n_users = len(self.usernames)
        source = np.repeat(np.arange(n_users), n_users).tolist()
        target = np.arange(n_users, 2*n_users).tolist()*n_users
        value = responses.values.flatten().tolist()

        # Get figure
        fig = fig_sankey(
            label=label,
            color=color,
            source=source,
            target=target,
            value=value,
            title=title
        )
        return fig

    def user_message_responses_heatmap(self, title="Response matrix"):
        """Get the response matrix heatmap.

        A response is from user X to user Y happens if user X sends a message right after message Y does.

        This method generates a plotly-ready figure (as a dictionary) using Heatmaps.

        Args:
            title (str, optional): Title for plot. Defaults to "Response matrix".

        Returns:
            dict: Dictionary with data and layout. Plotly compatible

        Example:

            ```python
            >>> from whatstk import df_from_txt
            >>> from whatstk.graph import plot, FigureBuilder
            >>> filename = 'path/to/samplechat.txt'
            >>> df = df_from_txt(filename)
            >>> fig = FigureBuilder(df).user_message_responses_heatmap()
            >>> plot(fig)
            ```

        """
        # Get response matrix
        responses = response_matrix(self.df)

        # Get figure
        fig = fig_heatmap(
            df_matrix=responses,
            title=title
        )
        return fig
