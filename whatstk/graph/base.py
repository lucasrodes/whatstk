"""Build plotly-compatible figures."""


import numpy as np
from whatstk._chat import BaseChat
from whatstk.analysis.interventions import get_interventions_count
from whatstk.analysis.responses import get_response_matrix, NORMS
from whatstk.graph.figures.scatter import fig_scatter_time
from whatstk.graph.figures.boxplot import fig_boxplot_msglen
from whatstk.graph.figures.sankey import fig_sankey
from whatstk.graph.figures.heatmap import fig_heatmap
from whatstk.graph.figures.utils import hex_color_palette
from whatstk.utils.utils import _get_df


class FigureBuilder:
    """Generate a variety of figures from your loaded chat.

    Integrates feature extraction and visualization logic to automate data plots.

    **Note**: Either ``df`` or ``chat`` must be provided.

    Args:
        df (pandas.DataFrame, optional): Chat data. Atribute `df` of a chat loaded using Chat. If a value is given,
                                            ``chat`` is ignored.
        chat (Chat, optional): Chat data. Object obtained when chat loaded using Chat. Required if ``df`` is None.

    """

    def __init__(self, df=None, chat=None):
        """Constructor.

        Args:
            df (pandas.DataFrame, optional): Chat data. Atribute `df` of a chat loaded using Chat. If a value is given,
                                            ``chat`` is ignored.
            chat (Chat, optional): Chat data. Object obtained when chat loaded using Chat. Required if ``df`` is None.

        """
        self.df = _get_df(df=df, chat=chat)
        self.__user_color_mapping = None

    @property
    def usernames(self):
        """Get list with users available in given chat.

        Returns:
            list: List with usernames available in chat DataFrame.

        """
        return BaseChat(df=self.df).users

    @property
    def user_color_mapping(self):
        """Get mapping between user and color.

        Each user is assigned a color automatically, so that this color is preserved for that user in all
        to-be-generated plots.

        Returns:
            dict: Mapping from username to color (rgb).

        """
        if self.__user_color_mapping is None:
            colors = hex_color_palette(n_colors=len(self.usernames))
            mapping = dict(zip(self.usernames, colors))
            return mapping
        return self.__user_color_mapping

    @user_color_mapping.setter
    def user_color_mapping(self, value):
        self.__user_color_mapping = value

    def user_msg_length_boxplot(self, title="User message length", xlabel="User"):
        """Generate figure with boxplots of each user's message length.

        Args:
            title (str, optional): Title for plot. Defaults to "User message length".
            xlabel (str, optional): x-axis label title. Defaults to "User".

        Returns:
            dict: Dictionary with data and layout. Plotly compatible.

        ..  seealso::

            * :func:`fig_boxplot_msglen <whatstk.graph.figures.boxplot.fig_boxplot_msglen>`

        Example:
            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.graph import plot, FigureBuilder
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
                >>> fig = FigureBuilder(chat=chat).user_msg_length_boxplot()
                >>> plot(fig)

        """
        fig = fig_boxplot_msglen(
            df=self.df,
            username_to_color=self.user_color_mapping,
            title=title,
            xlabel=xlabel
        )
        return fig

    def user_interventions_count_linechart(self, date_mode='date', msg_length=False, cumulative=False, all_users=False,
                                           title="User interventions count", xlabel="Date/Time", cummulative=None):
        """Plot number of user interventions over time.

        Args:
            date_mode (str, optional): Choose mode to group interventions by. Defaults to ``'date'``. Available modes
                                        are:

                                        - ``'date'``: Grouped by particular date (year, month and day).
                                        - ``'hour'``: Grouped by hours.
                                        - ``'month'``: Grouped by months.
                                        - ``'weekday'``: Grouped by weekday (i.e. monday, tuesday, ..., sunday).
                                        - ``'hourweekday'``: Grouped by weekday and hour.
            msg_length (bool, optional): Set to True to count the number of characters instead of number of messages
                                         sent.
            cumulative (bool, optional): Set to True to obtain commulative counts.
            all_users (bool, optional): Obtain number of interventions of all users combined. Defaults to False.
            title (str, optional): Title for plot. Defaults to "User interventions count".
            xlabel (str, optional): x-axis label title. Defaults to "Date/Time".
            cummulative (bool, optional): Deprecated, use cumulative.

        Returns:
            plotly.graph_objs.Figure: Plotly Figure.

        ..  seealso::

            * :func:`get_interventions_count <whatstk.analysis.get_interventions_count>`
            * :func:`fig_scatter_time <whatstk.graph.figures.scatter.fig_scatter_time>`

        Example:
            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.graph import plot, FigureBuilder
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
                >>> fig = FigureBuilder(chat=chat).user_interventions_count_linechart(cumulative=True)
                >>> plot(fig)

        """
        counts = get_interventions_count(
            df=self.df,
            date_mode=date_mode,
            msg_length=msg_length,
            cumulative=cumulative,
            all_users=all_users,
            cummulative=cummulative
        )
        if all_users:
            fig = fig_scatter_time(
                user_data=counts,
                title=title,
                xlabel=xlabel
            )
        else:
            fig = fig_scatter_time(
                user_data=counts,
                username_to_color=self.user_color_mapping,
                title=title,
                xlabel=xlabel
            )
        return fig

    def user_message_responses_flow(self, title="Message flow"):
        """Get the flow of message responses.

        A response from user X to user Y happens if user X sends a message right after a message from user Y.

        Uses a Sankey diagram.

        Args:
            title (str, optional): Title for plot. Defaults to "Message flow".

        Returns:
            plotly.graph_objs.Figure: Plotly Figure.

        ..  seealso::

            * :func:`get_response_matrix <whatstk.analysis.get_response_matrix>`
            * :func:`fig_sankey <whatstk.graph.figures.sankey.fig_sankey>`

        Example:
            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.graph import plot, FigureBuilder
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
                >>> fig = FigureBuilder(chat=chat).user_message_responses_flow()
                >>> plot(fig)

        """
        # Get response matrix
        responses = get_response_matrix(self.df)

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

    def user_message_responses_heatmap(self, norm=NORMS.ABSOLUTE, title="Response matrix"):
        """Get the response matrix heatmap.

        A response from user X to user Y happens if user X sends a message right after a message from user Y.

        Args:
            norm (str, optional): Specifies the type of normalization used for reponse count. Can be:

                                - ``'absolute'``: Absolute count of messages.
                                - ``'joint'``: Normalized by total number of messages sent by all users.
                                - ``'sender'``: Normalized per sender by total number of messages sent by user.
                                - ``'receiver'``: Normalized per receiver by total number of messages sent by user.
            title (str, optional): Title for plot. Defaults to "Response matrix".

        Returns:
            plotly.graph_objs.Figure: Plotly Figure.

        ..  seealso::

            * :func:`get_response_matrix <whatstk.analysis.get_response_matrix>`
            * :func:`fig_heatmap <whatstk.graph.figures.heatmap.fig_heatmap>`

        Example:
            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.graph import plot, FigureBuilder
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
                >>> fig = FigureBuilder(chat=chat).user_message_responses_heatmap()
                >>> plot(fig)

        """
        # Get response matrix
        responses = get_response_matrix(self.df, norm=norm)

        # Get figure
        fig = fig_heatmap(
            df_matrix=responses,
            title=title
        )
        return fig
