"""Base analysis tools."""


import pandas as pd
from whatstk.utils.utils import COLNAMES_DF, _get_df


def get_interventions_count(df=None, chat=None, date_mode='date', msg_length=False, cummulative=False):
    """Get number of interventions per user per unit of time.

    The unit of time can be chosen by means of argument `date_mode`.

    Example:

        Get counts of sent messages per user. Also cumulative.

        ```python
        >>> from whatstk import df_from_txt
        >>> from whatstk.analysis get_interventions_count
        >>> filename = 'path/to/samplechat.txt'
        >>> df = df_from_txt(filename)
        >>> counts = get_interventions_count(df=df, date_mode='date', msg_length=False)
        >>> counts_cumsum = counts.cumsum()
        ```

    Args:
        df (pandas.DataFrame): Chat as DataFrame.
        chat (WhatsAppChat): Object containing parsed WhatsApp chat.
        date_mode (str, optional): Choose mode to group interventions by. Defaults to 'date'. Available modes are:
                            - 'date': Grouped by particular date (year, month and day).
                            - 'hour': Grouped by hours.
                            - 'month': Grouped by months.
                            - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
                            - 'hourweekday': Grouped by weekday and hour.
        msg_length (bool, optional): Set to True to count the number of characters instead of number of messages sent.
        cummulative (bool, optional): Set to True to obtain commulative counts.

    Returns:
        pandas.DataFrame: DataFrame with shape NxU, where N: number of time-slots and U: number of users.

    Raises:
        ValueError: if `date_mode` value is not supported.

    """
    df = _get_df(df=df, chat=chat)

    if date_mode == 'date':
        n_interventions = _interventions(df, [df.index.date], msg_length)
        n_interventions.index = pd.to_datetime(n_interventions.index)
    elif date_mode == 'hour':
        n_interventions = _interventions(df, [df.index.hour], msg_length)
    elif date_mode == 'weekday':
        n_interventions = _interventions(df, [df.index.weekday], msg_length)
    elif date_mode == 'hourweekday':
        n_interventions = _interventions(df, [df.index.weekday, df.index.hour], msg_length)
    elif date_mode == 'month':
        n_interventions = _interventions(df, [df.index.month], msg_length)
    else:
        raise ValueError("Mode {} is not implemented. Valid modes are 'date', 'hour', 'weekday', "
                         "'hourweekday' and 'month".format(date_mode))

    if date_mode == 'hourweekday':
        n_interventions.index = n_interventions.index.set_names(['weekday', 'hour'])
    else:
        n_interventions.index.name = date_mode
    n_interventions.columns = n_interventions.columns.get_level_values(COLNAMES_DF.USERNAME)

    if cummulative:
        n_interventions = n_interventions.cumsum()

    return n_interventions


def _interventions(df, index_date, msg_length):
    """Get number of interventions per day per user.

    Args:
        df (pandas.DataFrame): Chat as DataFrame.

    Returns:
        pandas.DataFrame: Table with interventions per day per user.

    """
    if msg_length:
        counts_ = df.copy()
        counts_[COLNAMES_DF.MESSAGE_LENGTH] = counts_[COLNAMES_DF.MESSAGE].apply(lambda x: len(x))
        counts = counts_.groupby(by=index_date + [COLNAMES_DF.USERNAME]).agg({
            COLNAMES_DF.MESSAGE_LENGTH: lambda x: x.sum()
        })
    else:
        counts = df.groupby(by=index_date + [COLNAMES_DF.USERNAME]).agg('count')
    counts = counts.unstack(fill_value=0)

    return counts
