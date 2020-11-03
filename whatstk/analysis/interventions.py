"""Base analysis tools."""


import warnings
import pandas as pd
from whatstk.utils.utils import COLNAMES_DF, _get_df


def get_interventions_count(df=None, chat=None, date_mode='date', msg_length=False, cumulative=False, all_users=False,
                            cummulative=None):
    """Get number of interventions per user per unit of time.

    The unit of time can be chosen by means of argument ``date_mode``.

    **Note**: Either ``df`` or ``chat`` must be provided.

    Args:
        df (pandas.DataFrame, optional): Chat data. Atribute `df` of a chat loaded using Chat. If a value is given,
                                            ``chat`` is ignored.
        chat (Chat, optional): Chat data. Object obtained when chat loaded using Chat. Required if ``df`` is None.
        date_mode (str, optional): Choose mode to group interventions by.
                                    Defaults to ``date_mode=date``. Available modes are:

                                    - ``'date'``: Grouped by particular date (year, month and day).
                                    - ``'hour'``: Grouped by day hours (24 hours).
                                    - ``'month'``: Grouped by months (12 months).
                                    - ``'weekday'``: Grouped by weekday (i.e. monday, tuesday, ..., sunday).
                                    - ``'hourweekday'``: Grouped by weekday and hour.
        msg_length (bool, optional): Set to True to count the number of characters instead of number of messages sent.
        cumulative (bool, optional): Set to True to obtain commulative counts.
        all_users (bool, optional): Obtain number of interventions of all users combined. Defaults to False.
        cummulative (bool, optional): Deprecated, use cumulative.

    Returns:
        pandas.DataFrame: DataFrame with shape *NxU*, where *N*: number of time-slots and *U*: number of users.

    Raises:
        ValueError: if ``date_mode`` value is not supported.

    Example:
            Get number of interventions per user from `POKEMON chat
            <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/pokemon.txt>`_. The counts are
            represented as a `NxU` matrix, where `N`: number of time-slots and `U`: number of users.

            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.analysis import get_interventions_count
                >>> from whatstk.data import whatsapp_urls
                >>> filepath = whatsapp_urls.POKEMON
                >>> chat = WhatsAppChat.from_source(filepath)
                >>> counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False)
                >>> counts.head(5)
                username    Ash Ketchum  Brock  Jessie & James  ...  Prof. Oak  Raichu  Wobbuffet
                date                                            ...
                2016-08-06            2      2               0  ...          0       0          0
                2016-08-07            1      1               0  ...          1       0          0
                2016-08-10            1      0               1  ...          0       2          0
                2016-08-11            0      0               0  ...          0       0          0
                2016-09-11            0      0               0  ...          0       0          0

                [5 rows x 8 columns]

    """
    if cummulative is not None:
        cumulative = cummulative
        warnings.warn("cummulative is deprecated and will be removed in v0.4.0; use cumulative", DeprecationWarning)

    df = _get_df(df=df, chat=chat)

    if date_mode == 'date':
        n_interventions = _interventions(df, [df[COLNAMES_DF.DATE].dt.date], msg_length)
        n_interventions.index = pd.to_datetime(n_interventions.index)
        print(n_interventions.shape)
    elif date_mode == 'hour':
        n_interventions = _interventions(df, [df[COLNAMES_DF.DATE].dt.hour], msg_length)
    elif date_mode == 'weekday':
        n_interventions = _interventions(df, [df[COLNAMES_DF.DATE].dt.weekday], msg_length)
    elif date_mode == 'hourweekday':
        n_interventions = _interventions(df, [df[COLNAMES_DF.DATE].dt.weekday, df[COLNAMES_DF.DATE].dt.hour],
                                         msg_length)
    elif date_mode == 'month':
        n_interventions = _interventions(df, [df[COLNAMES_DF.DATE].dt.month], msg_length)
    else:
        raise ValueError("Mode {} is not implemented. Valid modes are 'date', 'hour', 'weekday', "
                         "'hourweekday' and 'month'.".format(date_mode))

    if date_mode == 'hourweekday':
        n_interventions.index = n_interventions.index.set_names(['weekday', 'hour'])
    else:
        n_interventions.index.name = date_mode
    n_interventions.columns = n_interventions.columns.get_level_values(COLNAMES_DF.USERNAME)

    if all_users:
        n_interventions = pd.DataFrame(n_interventions.sum(axis=1), columns=['interventions count'])
    if cumulative:
        n_interventions = n_interventions.cumsum()

    return n_interventions


def _interventions(df, series_tf, msg_length):
    """Get number of interventions per date per user.

    Args:
        df (pandas.DataFrame): Chat as DataFrame.
        series_tf (list): List of pandas series with the date transformations applied, so we can group by, e.g., month.
        msg_length (bool, optional): Set to True to count the number of characters instead of number of messages sent.

    Returns:
        pandas.DataFrame: Table with interventions per day per user.

    """
    if msg_length:
        counts_ = df.copy()
        counts_[COLNAMES_DF.MESSAGE_LENGTH] = counts_[COLNAMES_DF.MESSAGE].apply(lambda x: len(x))
        counts = counts_.groupby(by=series_tf+[COLNAMES_DF.USERNAME]).agg({
            COLNAMES_DF.MESSAGE_LENGTH: lambda x: x.sum()
        })
    else:
        counts = df.groupby(by=series_tf + [COLNAMES_DF.USERNAME]).agg({'message': 'count'})
    counts = counts.unstack(fill_value=0)

    return counts
