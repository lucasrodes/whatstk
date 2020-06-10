"""Library objects."""


from whatstk._chat import BaseChat
from whatstk.utils.chat_merge import merge_chats
from whatstk.whatsapp.parser import df_from_txt_whatsapp


class WhatsAppChat(BaseChat):
    """Use this class to load and process your chat text file.

    Attributes:
        df: Chat as pandas.DataFrame.

    """

    def __init__(self, df):
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.

        """
        super().__init__(df, platform='whatsapp')

    @classmethod
    def from_txt(cls, filename, **kwargs):
        """Create instance from chat log txt file hosted locally.

        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        ..  seealso::

            * :func:`df_from_txt_whatsapp <whatstk.whatsapp.parser.df_from_txt_whatsapp>`
        """
        # Prepare DataFrame
        df = df_from_txt_whatsapp(filename=filename, **kwargs)

        return cls(df)

    @classmethod
    def from_multiple_txt(cls, filenames, auto_header=None, hformat=None, encoding='utf-8'):
        """Load a WhatsAppChat instance from multiple sources.

        Args:
            filenames (list): List with paths to chat text files, e.g. ['part1.txt', 'part2.txt', ...].
            auto_header (bool, optional): Detect header automatically (applies to all files). If None, attempts to
                                            perform automatic header detection for all files. If False, ``hformat`` is
                                            required.
            hformat (list, optional): List with the :ref:`header format <The header format>` to be used for each file.
                                        The list must be of length equal to ``len(filenames)``. A valid header format
                                        might be '[%y-%m-%d %H:%M:%S] - %name:'.
            encoding (str): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        ..  seealso::

            * :func:`df_from_txt_whatsapp <whatstk.whatsapp.parser.df_from_txt_whatsapp>`
            * :func:`WhatsAppChat.from_txt <WhatsAppChat.from_txt>`
            * :func:`merge_chats <whatstk.utils.chat_merge.merge_chats>`

        Example:
            Load a chat from two chat text files ('path/to/chat1.txt' and 'path/to/chat2.txt').

            ..  code-block:: python

                >>> from whatstk.whatsapp.objects import WhatsAppChat
                >>> filename1 = 'path/to/chat1.txt'
                >>> filename2 = 'path/to/chat2.txt'
                >>> df = WhatsAppChat.from_multiple_txt([filename1, filename2])
        """
        dfs = []
        if auto_header is None or auto_header:
            auto_header = [True]*len(filenames)
        else:
            auto_header = [False]*len(filenames)
        if hformat is None:
            hformat = [None]*len(filenames)
        for filename, ah, hf in zip(filenames, auto_header, hformat):
            chat = WhatsAppChat.from_txt(filename, auto_header=ah, hformat=hf, encoding=encoding)
            dfs.append(chat.df)
        df = merge_chats(dfs)
        return cls(df)

    def to_txt(self, filename, hformat=None):
        """Export chat as txt file.

        Usefull to export the chat to different formats.

        Args:
            hformat (str, optional): Header format. Defaults to "%y-%m-%d, %H:%M - %name:".
            filename (str): Name of the file to export.

        """
        if not filename.endswith('.txt'):
            raise ValueError("filename must end with .txt")
        if not hformat:
            hformat = "%y-%m-%d, %H:%M - %name:"
        lines = []
        raw_lines = self.df.reset_index().values.tolist()
        for line in raw_lines:
            date, user, text = line
            hformat = hformat.replace('%name', '{name}')
            header = date.strftime(hformat).format(name=user)
            formatted_line = '{} {}'.format(header, text)
            lines.append(formatted_line)
        text = '\n'.join(lines)
        with open(filename, 'w') as f:
            f.write(text)
