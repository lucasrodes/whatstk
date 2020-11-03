"""Library WhatsApp objects."""


from whatstk._chat import BaseChat
from whatstk.utils.chat_merge import merge_chats
from whatstk.whatsapp.parser import df_from_txt_whatsapp


class WhatsAppChat(BaseChat):
    """Load and process a WhatsApp chat file.

    Args:
        df (pandas.DataFrame): Chat.

    Example:
        This simple example loads a chat using :func:`WhatsAppChat <WhatsAppChat>`. Once loaded, we can access its
        attribute :func:`df <WhatsAppChat.df>`, which contains the loaded chat as a DataFrame.

        ..  code-block:: python

            >>> from whatstk.whatsapp.objects import WhatsAppChat
            >>> from whatstk.data import whatsapp_urls
            >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON)
            >>> chat.df.head(5)
                             date     username                                            message
            0 2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
            1 2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
            2 2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
            3 2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
            4 2016-08-06 14:30:00        Misty                                          Definetly

    """
    def __init__(self, df):
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.

        """
        super().__init__(df, platform='whatsapp')

    @classmethod
    def from_source(cls, filepath, **kwargs):
        """Create an instance from a chat text file.

        Args:
            filepath (str): Path to the file. It can be a local file (e.g. 'path/to/file.txt') or an URL to a hosted
                            file (e.g. 'http://www.url.to/file.txt')
            **kwargs: Refer to the docs from
                        :func:`df_from_txt_whatsapp <whatstk.whatsapp.parser.df_from_txt_whatsapp>` for details on
                        additional arguments.

        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        ..  seealso::

            * :func:`df_from_txt_whatsapp <whatstk.whatsapp.parser.df_from_txt_whatsapp>`
            * :func:`WhatsAppChat.from_sources <whatstk.WhatsAppChat.from_sources>`

        """
        # Prepare DataFrame
        df = df_from_txt_whatsapp(filepath=filepath, **kwargs)

        return cls(df)

    @classmethod
    def from_sources(cls, filepaths, auto_header=None, hformat=None, encoding='utf-8'):
        """Load a WhatsAppChat instance from multiple sources.

        Args:
            filepaths (list): List with filepaths.
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

            * :func:`WhatsAppChat.from_source <WhatsAppChat.from_source>`
            * :func:`merge_chats <whatstk.utils.chat_merge.merge_chats>`

        Example:
            Load a chat using two text files. In this example, we use sample chats (available online, see urls in
            source code :mod:`whatstk.data <whatstk.data>`).

            ..  code-block:: python

                >>> from whatstk.whatsapp.objects import WhatsAppChat
                >>> from whatstk.data import whatsapp_urls
                >>> filepath_1 = whatsapp_urls.LOREM1
                >>> filepath_2 = whatsapp_urls.LOREM2
                >>> chat = WhatsAppChat.from_sources(filepaths=[filepath_1, filepath_2])
                >>> chat.df.head(5)
                                 date        username                                            message
                0 2019-10-20 10:16:00            John        Laborum sed excepteur id eu cillum sunt ut.
                1 2019-10-20 11:15:00            Mary  Ad aliquip reprehenderit proident est irure mo...
                2 2019-10-20 12:16:00  +1 123 456 789  Nostrud adipiscing ex enim reprehenderit minim...
                3 2019-10-20 12:57:00  +1 123 456 789  Deserunt proident laborum exercitation ex temp...
                4 2019-10-20 17:28:00            John                Do ex dolor consequat tempor et ex.

        """
        dfs = []
        if auto_header is None or auto_header:
            auto_header = [True]*len(filepaths)
        else:
            auto_header = [False]*len(filepaths)
        if hformat is None:
            hformat = [None]*len(filepaths)
        for filepath, ah, hf in zip(filepaths, auto_header, hformat):
            chat = WhatsAppChat.from_source(filepath, auto_header=ah, hformat=hf, encoding=encoding)
            dfs.append(chat.df)
        df = merge_chats(dfs)
        return cls(df)

    def to_txt(self, filepath, hformat=None):
        """Export chat to a text file.

        Usefull to export the chat to different formats (i.e. using different hformats).

        Args:
            filepath (str): Name of the file to export (must be a local path).
            hformat (str, optional): Header format. Defaults to '%y-%m-%d, %H:%M - %name:'.

        """
        if not filepath.endswith('.txt'):
            raise ValueError("filepath must end with .txt")
        if not hformat:
            hformat = "%y-%m-%d, %H:%M - %name:"
        lines = []
        raw_lines = self.df.values.tolist()
        for line in raw_lines:
            date, user, text = line
            hformat = hformat.replace('%name', '{name}')
            header = date.strftime(hformat).format(name=user)
            formatted_line = '{} {}'.format(header, text)
            lines.append(formatted_line)
        text = '\n'.join(lines)
        with open(filepath, 'w') as f:
            f.write(text)
