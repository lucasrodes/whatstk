"""Build plotly-compatible figures."""


from whatstk.objects import WhatsAppChat
from whatstk.analysis import get_interventions_count
from whatstk.plotly.figures.scatter import fig_scatter_time
from whatstk.plotly.figures.boxplot import fig_boxplot_msglen
from whatstk.plotly.figures.utils import hex_color_palette


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
        self.df = self._get_df(df=df, chat=chat)

    def _get_df(self, df, chat):
        if (df is None) & (chat is None):
            raise ValueError("Please provide a chat, using either argument `df` or argument `chat`.")
        if (df is None) and (chat is not None):
            df = chat.df
        return df

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
            >>> from whatstk.plotly import plot, FigureBuilder
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
            >>> from whatstk.plotly import plot, FigureBuilder
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
