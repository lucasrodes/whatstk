"""Utils."""


from collections import namedtuple


ColnamesDf = namedtuple('Constants', ['DATE', 'USERNAME', 'MESSAGE', 'MESSAGE_LENGTH'])
COLNAMES_DF = ColnamesDf(
    DATE='date',
    USERNAME='username',
    MESSAGE='message',
    MESSAGE_LENGTH='message_length'
)


def _get_df(df, chat):
    if (df is None) & (chat is None):
        raise ValueError("Please provide a chat, using either argument `df` or `chat`.")
    if (df is None) and (chat is not None):
        df = chat.df
    return df
