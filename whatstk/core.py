"""For backwards compatibility"""


from whatstk.objects import WhatsAppChat
from whatstk.analysis import interventions


def df_from_txt(filename, auto_header=True, hformat=None, encoding='utf-8'):
    """Load the chat log text file as a pandas.DataFrame.
        
    Args:

        filename (str): Name to the txt chat log file.
        auto_header (bool): Set to True to detect header automatically, otherwise set to False. Defaults to True. If
                            False, you have to provide a value to `hformat`.
        hformat (str): Format of the header. Check `whatstk.WhatsAppChat.prepare_df` docs.
        encoding (str): Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
        
    Returns:
        pandas.DataFrame: Chat in DataFrame format with following columns: date (index), username, message.

    """
    chat = WhatsAppChat.from_txt(
        filename=filename,
        auto_header=auto_header,
        hformat=hformat,
        encoding=encoding
    )
    return chat.df