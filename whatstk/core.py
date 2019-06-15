from .alpha.parser import generate_regex, parse_chat, fix_df
from .alpha.exceptions import *
import pandas as pd


class WhatsAppChat:
    """Use this class to load and play with your chat log."""

    def __init__(self, df):
        """Constructor."""
        self.df = df
        self.users = self.df.username.unique().tolist()

    @classmethod
    def from_txt(cls, filename, hformat, encoding='utf-8'):
        """Create instance from chat log txt file hosted locally.

        :param filename: Name to the txt chat log file.
        :type filename: str
        :param hformat: Format of the header. Check whatstk.WhatsAppChat.prepare_df docs.
        :type hformat: str
        :param encoding: Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
        :type encoding: str
        :return: WhatsAppChat instance with loaded and parsed chat.
        :rtype: whatstk.core.WhatsAppChat
        """
        # read file
        with open(filename, encoding=encoding) as f:
            text = f.read()

        # Prepare DataFrame
        df = cls.prepare_df(text, hformat)

        return cls(df)

    @staticmethod
    def prepare_df(text, hformat):
        """Get a DataFrame-formatted chat.

        :param text: Loaded chat as plain text.
        :type text: str
        :param hformat: Format of the header. Ude the following keywords:
                        - %y: for year.
                        - %m: for month.
                        - %d: for day.
                        - %H: for hour.
                        - %M: for minutes.
                        - %S: for seconds.
                        - %P: To denote 12h clock.
                        - %name: for the username

                        Example 1: To the header '12/08/2016, 16:20 - username:' corresponds the syntax
                        '%d/%m/%y, %H:%M - %name:'.

                         Example 2: To the header '2016-08-12, 4:20 PM - username:' corresponds the syntax
                        '%y-%m-%d, %H:%M %P - %name:'.
        :type hformat: str
        :return: DataFrame containing the chat.
        :rtype: pandas.DataFrame
        """
        # generate regex
        r, r_x = generate_regex(hformat=hformat)

        #  parse chat to DataFrame
        df = parse_chat(text, r)

        # get rid of wp warning messages
        return fix_df(r_x, df)

    def to_csv(self, filename):
        """Save data as csv.

        :param filename: Name of file.
        :type filename: str
        """
        self.df.to_csv(filename)

    def __len__(self):
        """Get length of DataFrame

        :return: Length.
        :rtype: int
        """
        return len(self.df)

    def shape(self):
        """Get shape of DataFrame-formatted chat.

        :return: Shape.
        :rtype: tuple
        """
        return self.df.shape


def interventions(chat, date_mode='date', msg_length=False):
    """Get number of interventions per user per unit of time.

    The unit of time can be chosen by means of argument `date_mode`.

    :Example: Get counts of sent messages per user. Also cumulative.

        >>> from whatstk.core import WhatsAppChat, interventions
        >>> filename = 'path/to/samplechat.txt'
        >>> hformat = '%d/%m/%y, %H:%M - %name:'
        >>> chat = WhatsAppChat.from_txt(filename, hformat)
        >>> counts = interventions(chat, 'date', msg_length=False)
        >>> counts_cumsum = counts.cumsum()

    :param chat: Object containing parsed WhatsApp chat.
    :type chat: whatstk.WhatsAppChat
    :param date_mode: Choose mode to group interventions by. Available modes are:
                        - 'date': Grouped by particular date (year, month and day).
                        - 'hour': Grouped by hours.
                        - 'month': Grouped by months.
                        - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
                        - 'hourweekday': Grouped by weekday and hour.
    :type date_mode: str
    :param msg_length: Set to True to count the number of characters instead of number of messages sent.
    :type msg_length: bool
    :return: DataFrame with shape NxU, where N: number of time-slots and U: number of users.
    :rtype: pandas.DataFrame
    :raises whatstk.exceptions.InterventionModeError: if invalid mode is chosen.
    """
    if date_mode == 'date':
        n_interventions = _interventions(chat, [chat.df.index.date], msg_length)
        n_interventions.index = pd.to_datetime(n_interventions.index)
    elif date_mode == 'hour':
        n_interventions = _interventions(chat, [chat.df.index.hour], msg_length)
    elif date_mode == 'weekday':
        n_interventions = _interventions(chat, [chat.df.index.weekday], msg_length)
    elif date_mode == 'hourweekday':
        n_interventions = _interventions(chat, [chat.df.index.weekday, chat.df.index.hour], msg_length)
    elif date_mode == 'month':
        n_interventions = _interventions(chat, [chat.df.index.month], msg_length)
    else:
        raise InterventionModeError("Mode {} is not implemented. Valid modes are 'date', 'hour', 'weekday', "
                                    "'hourweekday' and 'month".format(date_mode))

    n_interventions.index.name = date_mode
    n_interventions.columns = n_interventions.columns.get_level_values('username')
    return n_interventions


def _interventions(chat, index_date, msg_length):
    """Get number of interventions per day per user

    :param chat: Chat.
    :type chat: whatstk.core.WhatsAppChat
    :return: Table with interventions per day per user.
    :rtype: pandas.DataFrame
    """
    if msg_length:
        counts_ = chat.df.copy()
        counts_['message_length'] = counts_['message'].apply(lambda x: len(x))
        counts = counts_.groupby(by=index_date + ['username']).agg({'message_length': lambda x: x.sum()})
    else:
        counts = chat.df.groupby(by=index_date + ['username']).agg('count')
    counts = counts.unstack(fill_value=0)

    return counts


