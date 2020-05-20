"""Text to dataframe methods."""


from whatstk.objects import WhatsAppChat


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

    Example:

        ```python
        >>>  from whatstk import df_from_txt
        >>> filename = 'path/to/chat.txt'
        >>> df = df_from_txt(filename)
        ```

    """
    chat = WhatsAppChat.from_txt(
        filename=filename,
        auto_header=auto_header,
        hformat=hformat,
        encoding=encoding
    )
    return chat.df


def df_from_multiple_txt(filenames, auto_header=None, hformat=None, encoding='utf-8'):
    """Load the chat log text file as a pandas.DataFrame using multiple txt sources.

    The merge is done time-wise. See method whatstk.utils.chat_merge.merge_chats for more details on the merge
    impementation.

    Args:

        filenames (list): List with names of the files, e.g. ['part1.txt', 'part2.txt', ...].
        auto_header (list, optional): Whether auto_header should be performed (for each file, choose True/False).
                                            Defaults to True for all files.
        hformat (list, optional): List with the hformat to be used per each file. Defaults to None.
        encoding (str, optional): Encoding to use when loading file. Defaults to 'utf-8'.

    Returns:
        pandas.DataFrame: Chat in DataFrame format with following columns: date (index), username, message.

    Example:

        ```python
        >>>  from whatstk import df_from_multiple_txt
        >>> filename1 = 'path/to/chat1.txt'
        >>> filename2 = 'path/to/chat2.txt'
        >>> df = df_from_multiple_txt([filename1, filename2])
        ```

    """
    chat = WhatsAppChat.from_multiple_txt(
        filenames=filenames,
        auto_header=auto_header,
        hformat=hformat,
        encoding=encoding
    )
    return chat.df
